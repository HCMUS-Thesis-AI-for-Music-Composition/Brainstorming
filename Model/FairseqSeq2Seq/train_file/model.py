from fairseq.tasks.language_modeling import LanguageModelingTask, LanguageModelingConfig
from fairseq.tasks import register_task
from fairseq.models.transformer_lm import TransformerLanguageModelConfig, TransformerLanguageModel,base_lm_architecture, DEFAULT_MAX_TARGET_POSITIONS
from fairseq.models import (
    FairseqLanguageModel,
    register_model,
    register_model_architecture,
)
from fairseq.models.transformer import (
    DEFAULT_MIN_PARAMS_TO_WRAP,
    Embedding,
    TransformerDecoder,
)
import torch
from fairseq.utils import safe_getattr, safe_hasattr
from fairseq import options, utils, search
from dataload import CommandDataset
import numpy as np
from fairseq.models import FairseqDecoder
from fairseq.modules.transformer_layer import TransformerDecoderLayer, TransformerEncoderLayer
from typing import Dict, List, Optional
from fast_transformers.attention.attention_layer import AttentionLayer
from fast_transformers.attention.causal_linear_attention import CausalLinearAttention
from fairseq.models.transformer import Linear
import math, gc
from typing import Any, Dict, List, Optional
import torch
import torch.nn as nn
from torch import Tensor
from torch.utils.checkpoint import checkpoint
from fairseq import utils
from fairseq.models.fairseq_encoder import EncoderOut
from fairseq.modules import (
    AdaptiveSoftmax,
    FairseqDropout,
    LayerDropModuleList,
    LayerNorm,
    PositionalEmbedding,
    SinusoidalPositionalEmbedding,
    AdaptiveInput, CharacterTokenEmbedder
)
from fairseq.modules.quant_noise import quant_noise as apply_quant_noise_
from typing import Dict, List, Optional
from torch import Tensor
from fairseq.modules.transformer_layer import TransformerDecoderLayer, TransformerEncoderLayer
from fast_transformers.attention.causal_linear_attention import CausalLinearAttention
from fast_transformers.attention.attention_layer import AttentionLayer
from fast_transformers.attention import LinearAttention
from attention_fast import CustomAttentionLayer
from fast_transformers.masking import LengthMask
from fast_transformers.masking import TriangularCausalMask

class CasualTransformerModel(TransformerLanguageModel):
  @classmethod
  def add_args(cls, parser):
    super().add_args(parser)
    parser.add_argument('--gradient-checkpointing', type=lambda x: x.lower() == 'true', default=False)
    parser.add_argument('--gradient-checkpointing-every-n-layer', type=int, default=1)
    parser.add_argument('--gradient-checkpointing-layers',
                        type=lambda x: tuple([int(item) for item in x.split(',')]), default=None)
  @classmethod
  def build_model(cls, args, task):
    base_lm_architecture(args)
    if args.decoder_layers_to_keep:
        args.decoder_layers = len(args.decoder_layers_to_keep.split(","))
    if safe_getattr(args, "max_target_positions", None) is None:
            args.max_target_positions = safe_getattr(
                args, "tokens_per_sample", DEFAULT_MAX_TARGET_POSITIONS
            )

    if args.character_embeddings:
        embed_tokens = CharacterTokenEmbedder(
            task.source_dictionary,
            eval(args.character_filters),
            args.character_embedding_dim,
            args.decoder_embed_dim,
            args.char_embedder_highway_layers,
        )
    elif args.adaptive_input:
        embed_tokens = AdaptiveInput(
            len(task.source_dictionary),
            task.source_dictionary.pad(),
            args.decoder_input_dim,
            args.adaptive_input_factor,
            args.decoder_embed_dim,
            options.eval_str_list(args.adaptive_input_cutoff, type=int),
            args.quant_noise_pq,
            args.quant_noise_pq_block_size,
        )
    else:
        embed_tokens = cls.build_embedding(
            args, task.source_dictionary, args.decoder_input_dim
        )

    if args.tie_adaptive_weights:
        assert args.adaptive_input
        assert args.adaptive_input_factor == args.adaptive_softmax_factor
        assert (
            args.adaptive_softmax_cutoff == args.adaptive_input_cutoff
        ), "{} != {}".format(
            args.adaptive_softmax_cutoff, args.adaptive_input_cutoff
        )
        assert args.decoder_input_dim == args.decoder_output_dim

    decoder = TransformerDecoder(
        args, task.target_dictionary, embed_tokens, no_encoder_attn=True
    )
    return cls(decoder)

    @classmethod
    def build_embedding(cls, args, dictionary, embed_dim, path=None):
        embed_tokens = Embedding(len(dictionary), embed_dim, dictionary.pad())
        return embed_tokens
class CausualTransformerDecoderLayer(TransformerDecoderLayer):
    def __init__(self, args, no_encoder_attn=False, add_bias_kv=False, add_zero_attn=False):
        #args.num_heads = args.decoder_attention_heads
        print(args)
        super().__init__(args, no_encoder_attn=no_encoder_attn, add_bias_kv=add_bias_kv, add_zero_attn=add_zero_attn)
        self.decoder_attention_heads = args.decoder_attention_heads
        export = getattr(args, "char_inputs", False)

    def build_self_attention(
        self, embed_dim, args, add_bias_kv=False, add_zero_attn=False
    ):
        causal_linear_attention = CausalLinearAttention(embed_dim)
        linear_attention_layer = CustomAttentionLayer(causal_linear_attention,
                                                embed_dim, args.decoder_attention_heads)
        return linear_attention_layer

    def forward(
        self,
        x,
        encoder_out: Optional[torch.Tensor] = None,
        encoder_padding_mask: Optional[torch.Tensor] = None,
        incremental_state: Optional[Dict[str, Dict[str, Optional[Tensor]]]] = None,
        prev_self_attn_state: Optional[List[torch.Tensor]] = None,
        prev_attn_state: Optional[List[torch.Tensor]] = None,
        self_attn_mask: Optional[torch.Tensor] = None,
        self_attn_padding_mask: Optional[torch.Tensor] = None,
        need_attn: bool = False,
        need_head_weights: bool = False,
    ):
        """
        Args:
            x (Tensor): input to the layer of shape `(seq_len, batch, embed_dim)`
            encoder_padding_mask (ByteTensor, optional): binary
                ByteTensor of shape `(batch, src_len)` where padding
                elements are indicated by ``1``.
            need_attn (bool, optional): return attention weights
            need_head_weights (bool, optional): return attention weights
                for each head (default: return average over heads).

        Returns:
            encoded output of shape `(seq_len, batch, embed_dim)`
        """
        if need_head_weights:
            need_attn = True

        residual = x
        if self.normalize_before:
            x = self.self_attn_layer_norm(x)
        y = x

        x, attn = self.run_self_attn(
            query=x,
            key=y,
            value=y,
            key_padding_mask=self_attn_padding_mask,
            incremental_state=incremental_state,
            need_weights=False,
            attn_mask=self_attn_mask,
        )
        x = self.dropout_module(x)
        x = self.residual_connection(x, residual)
        if not self.normalize_before:
            x = self.self_attn_layer_norm(x)

        assert self.encoder_attn is None and encoder_out is None

        residual = x
        if self.normalize_before:
            x = self.final_layer_norm(x)

        x = self.activation_fn(self.fc1(x))
        x = self.activation_dropout_module(x)
        x = self.fc2(x)
        x = self.dropout_module(x)
        x = self.residual_connection(x, residual)
        if not self.normalize_before:
            x = self.final_layer_norm(x)
        if self.onnx_trace and incremental_state is not None:
            raise NotImplementedError
            saved_state = self.self_attn._get_input_buffer(incremental_state)
            assert saved_state is not None
            if self_attn_padding_mask is not None:
                self_attn_state = [
                    saved_state["prev_key"],
                    saved_state["prev_value"],
                    saved_state["prev_key_padding_mask"],
                ]
            else:
                self_attn_state = [saved_state["prev_key"], saved_state["prev_value"]]
            return x, attn, self_attn_state
        return x, attn, None

    def run_self_attn(self, query, key_padding_mask, incremental_state, need_weights, attn_mask, **kwargs):
        if incremental_state is not None:
            raise NotImplementedError
        if need_weights:
            raise NotImplementedError

        query = query.transpose(0, 1)

        if key_padding_mask is not None:
            key_padding_mask = ~key_padding_mask
        sequence_lengths = torch.tensor([query.shape[1]] * query.shape[0])  # Create a tensor with sequence lengths
        base_mask = LengthMask(sequence_lengths, device ="cuda:0")
        r = self.self_attn(query, query, query, attn_mask=attn_mask, key_padding_mask=key_padding_mask, key_len = base_mask)

        r = r.transpose(0, 1)

        return r, None


class CasualTransformerDecoder(FairseqDecoder):
    """
    Transformer decoder consisting of *args.decoder_layers* layers. Each layer
    is a :class:`TransformerDecoderLayer`.

    Args:
        args (argparse.Namespace): parsed command-line arguments
        dictionary (~fairseq.data.Dictionary): decoding dictionary
        embed_tokens (torch.nn.Embedding): output embedding
        no_encoder_attn (bool, optional): whether to attend to encoder outputs
            (default: False).
    """

    def __init__(self, args, dictionary, embed_tokens, no_encoder_attn=False):
        self.args = args
        super().__init__(dictionary)
        self.register_buffer("version", torch.Tensor([3]))
        # Sửa
        self.dropout_module = FairseqDropout(
            args.dropout, module_name=self.__class__.__name__
        )
        self.decoder_layerdrop = args.decoder_layerdrop
        # -------------
        self.share_input_output_embed = args.share_decoder_input_output_embed

        input_embed_dim = embed_tokens.embedding_dim
        embed_dim = args.decoder_embed_dim
        self.embed_dim = embed_dim
        self.output_embed_dim = args.decoder_output_dim

        self.padding_idx = embed_tokens.padding_idx
        self.max_target_positions = args.max_target_positions

        self.embed_tokens = embed_tokens

        self.embed_scale = 1.0 if args.no_scale_embedding else math.sqrt(embed_dim)
        # Sửa
        if not args.adaptive_input and args.quant_noise_pq > 0:
            self.quant_noise = apply_quant_noise_(
                nn.Linear(embed_dim, embed_dim, bias=False),
                args.quant_noise_pq,
                args.quant_noise_pq_block_size,
            )
        else:
            self.quant_noise = None
        # ----------------
        self.project_in_dim = (
            Linear(input_embed_dim, embed_dim, bias=False)
            if embed_dim != input_embed_dim
            else None
        )

        self.embed_positions = (
            PositionalEmbedding(
                8192,
                embed_dim,
                self.padding_idx,
                learned=args.decoder_learned_pos,
            )
            if not args.no_token_positional_embeddings
            else None
        )

        if getattr(args, "layernorm_embedding", False):
            self.layernorm_embedding = LayerNorm(embed_dim)
        else:
            self.layernorm_embedding = None

        self.cross_self_attention = getattr(args, "cross_self_attention", False)

        if self.decoder_layerdrop > 0.0:
            self.layers = LayerDropModuleList(p=self.decoder_layerdrop)
        else:
            self.layers = nn.ModuleList([])
        self.layers.extend(
            [
                self.build_decoder_layer(args, no_encoder_attn)
                for _ in range(args.decoder_layers)
            ]
        )
        self.num_layers = len(self.layers)

        if args.decoder_normalize_before and not getattr(
            args, "no_decoder_final_norm", False
        ):  # args.decoder_normalize_before default False
            self.layer_norm = LayerNorm(embed_dim)
        else:
            self.layer_norm = None
        # ------------------------------------
        self.project_out_dim = (
            Linear(embed_dim, self.output_embed_dim, bias=False)
            if embed_dim != self.output_embed_dim and not args.tie_adaptive_weights
            else None
        )

        self.adaptive_softmax = None
        self.output_projection = None
        if args.adaptive_softmax_cutoff is not None:
            self.adaptive_softmax = AdaptiveSoftmax(
                len(dictionary),
                self.output_embed_dim,
                utils.eval_str_list(args.adaptive_softmax_cutoff, type=int),
                dropout=args.adaptive_softmax_dropout,
                adaptive_inputs=embed_tokens if args.tie_adaptive_weights else None,
                factor=args.adaptive_softmax_factor,
                tie_proj=args.tie_adaptive_proj,
            )
        elif self.share_input_output_embed:
            self.output_projection = nn.Linear(
                self.embed_tokens.weight.shape[1],
                self.embed_tokens.weight.shape[0],
                bias=False,
            )
            self.output_projection.weight = self.embed_tokens.weight
        else:
            self.output_projection = nn.Linear(
                self.output_embed_dim, len(dictionary), bias=False
            )
            nn.init.normal_(
                self.output_projection.weight, mean=0, std=self.output_embed_dim**-0.5
            )

        self.gradient_checkpointing = getattr(
            self.args, "gradient_checkpointing", False
        )
        if self.gradient_checkpointing:
            checkpointing_layers = getattr(
                self.args, "gradient_checkpointing_layers", None
            )
            if checkpointing_layers is None:
                gradient_checkpointing_every_n_layer = getattr(
                    self.args, "gradient_checkpointing_every_n_layer", 1
                )
                checkpointing_layers = tuple(
                    range(0, self.num_layers, gradient_checkpointing_every_n_layer)
                )
            self.checkpointing_layers = checkpointing_layers

    def build_decoder_layer(self, args, no_encoder_attn=False):
        return CausualTransformerDecoderLayer(args, no_encoder_attn)

    def forward(
        self,
        prev_output_tokens,
        sep_pos,
        encoder_out: Optional[EncoderOut] = None,
        incremental_state: Optional[Dict[str, Dict[str, Optional[Tensor]]]] = None,
        features_only: bool = False,
        full_context_alignment: bool = False,
        alignment_layer: Optional[int] = None,
        alignment_heads: Optional[int] = None,
        src_lengths: Optional[Any] = None,
        return_all_hiddens: bool = False,
    ):
        """
        Args:
            prev_output_tokens (LongTensor): previous decoder outputs of shape
                `(batch, tgt_len)`, for teacher forcing
            encoder_out (optional): output from the encoder, used for
                encoder-side attention
            incremental_state (dict): dictionary used for storing state during
                :ref:`Incremental decoding`
            features_only (bool, optional): only return features without
                applying output layer (default: False).
            full_context_alignment (bool, optional): don't apply
                auto-regressive mask to self-attention (default: False).

        Returns:
            tuple:
                - the decoder's output of shape `(batch, tgt_len, vocab)`
                - a dictionary with any model-specific outputs
        """
        print("--------forward--------")
        x, extra = self.extract_features(
            prev_output_tokens,
            sep_pos,
            encoder_out=encoder_out,
            incremental_state=incremental_state,
            full_context_alignment=full_context_alignment,
            alignment_layer=alignment_layer,
            alignment_heads=alignment_heads,
        )
        if not features_only:
            x = self.output_layer(x)
        return x, extra

    def extract_features(
        self,
        prev_output_tokens,
        sep_pos,
        encoder_out: Optional[EncoderOut] = None,
        incremental_state: Optional[Dict[str, Dict[str, Optional[Tensor]]]] = None,
        full_context_alignment: bool = False,
        alignment_layer: Optional[int] = None,
        alignment_heads: Optional[int] = None,
    ):
        print(sep_pos)
        print("---------EXTRACT FEATURES ----------")
        return self.extract_features_scriptable(
            prev_output_tokens,
            sep_pos,
            encoder_out,
            incremental_state,
            full_context_alignment,
            alignment_layer,
            alignment_heads,
        )

    """
    A scriptable subclass of this class has an extract_features method and calls
    super().extract_features, but super() is not supported in torchscript. Aa copy of
    this function is made to be used in the subclass instead.
    """

    def extract_features_scriptable(
        self,
        prev_output_tokens,
        sep_pos,
        encoder_out: Optional[EncoderOut] = None,
        incremental_state: Optional[Dict[str, Dict[str, Optional[Tensor]]]] = None,
        full_context_alignment: bool = False,
        alignment_layer: Optional[int] = None,
        alignment_heads: Optional[int] = None,
    ):
        print(sep_pos)
        print('----extract_features_scriptable---')
        """
        Similar to *forward* but only return features.

        Includes several features from "Jointly Learning to Align and
        Translate with Transformer Models" (Garg et al., EMNLP 2019).

        Args:
            full_context_alignment (bool, optional): don't apply
                auto-regressive mask to self-attention (default: False).
            alignment_layer (int, optional): return mean alignment over
                heads at this layer (default: last layer).
            alignment_heads (int, optional): only average alignment over
                this many heads (default: all heads).

        Returns:
            tuple:
                - the decoder's features of shape `(batch, tgt_len, embed_dim)`
                - a dictionary with any model-specific outputs
        """
        if alignment_layer is None:
            alignment_layer = self.num_layers - 1

        # # embed positions
        # positions = (
        #     self.embed_positions(
        #         prev_output_tokens, incremental_state=incremental_state
        #     )
        #     if self.embed_positions is not None
        #     else None
        # )
        # SỬA
        if self.embed_positions is not None:
            if True: #not self.args.is_inference:
                positions = []
                for i, cut_pos in enumerate(sep_pos):
                    cur_word_positions = self.embed_positions(
                        prev_output_tokens[i : i + 1, cut_pos:], incremental_state=None
                    )
                    zeros_padding = torch.zeros(
                        [1, cut_pos, cur_word_positions.shape[2]]
                    ).to(cur_word_positions.device)
                    positions.append(
                        torch.cat([zeros_padding, cur_word_positions], dim=1)
                    )
                positions = torch.cat(positions, dim=0)
            else:
                positions = []
                for i, cut_pos in enumerate(sep_pos):
                    if (
                        prev_output_tokens.shape[1] > sep_pos[i]
                    ):  # sep_pos[i] means the absolute index
                        cur_word_positions = self.embed_positions(
                            prev_output_tokens[i : i + 1, cut_pos:],
                            incremental_state=None,
                        )
                        zeros_padding = torch.zeros(
                            [1, cut_pos, cur_word_positions.shape[2]]
                        ).to(cur_word_positions.device)
                        positions.append(
                            torch.cat([zeros_padding, cur_word_positions], dim=1)
                        )
                    else:
                        zeros_padding = torch.zeros(
                            [
                                1,
                                prev_output_tokens.shape[1],
                                self.args.decoder_embed_dim,
                            ]
                        ).to(prev_output_tokens.device)
                        positions.append(zeros_padding)
                positions = torch.cat(positions, dim=0)
        else:
            positions = None

        if incremental_state is not None:
            prev_output_tokens = prev_output_tokens[:, -1:]
            if positions is not None:
                positions = positions[:, -1:]

        # embed tokens and positions
        x = self.embed_scale * self.embed_tokens(prev_output_tokens)

        if self.quant_noise is not None:
            x = self.quant_noise(x)

        if self.project_in_dim is not None:
            x = self.project_in_dim(x)

        if positions is not None:
            x += positions

        if self.layernorm_embedding is not None:
            x = self.layernorm_embedding(x)

        x = self.dropout_module(x)

        # B x T x C -> T x B x C
        x = x.transpose(0, 1)

        self_attn_padding_mask: Optional[Tensor] = None
        if self.cross_self_attention or prev_output_tokens.eq(self.padding_idx).any():
            self_attn_padding_mask = prev_output_tokens.eq(self.padding_idx)

        # decoder layers
        attn: Optional[Tensor] = None
        inner_states: List[Optional[Tensor]] = [x]

        gradient_checkpointing_every_n_layer = getattr(
            self.args, "gradient_checkpointing_every_n_layer", 1
        )
        # Sửa
        for idx, layer in enumerate(self.layers):
            # if incremental_state is None and not full_context_alignment:
            #     self_attn_mask = self.buffered_future_mask(x)
            # else:
            #     self_attn_mask = None

            self_attn_mask = TriangularCausalMask(2)  # Casual Linear Attention does not need this

            if (
                getattr(self.args, "gradient_checkpointing", False)
                and self.training
                and idx in self.checkpointing_layers
            ):
                x, layer_attn, _ = checkpoint(
                    layer,
                    x,
                    encoder_out.encoder_out if encoder_out is not None else None,
                    (
                        encoder_out.encoder_padding_mask
                        if encoder_out is not None
                        else None
                    ),
                    incremental_state,
                    None,
                    None,
                    self_attn_mask,
                    self_attn_padding_mask,
                    bool((idx == alignment_layer)),
                    bool((idx == alignment_layer)),
                )
            else:
                x, layer_attn, _ = layer(
                    x,
                    encoder_out.encoder_out if encoder_out is not None else None,
                    (
                        encoder_out.encoder_padding_mask
                        if encoder_out is not None
                        else None
                    ),
                    incremental_state,
                    self_attn_mask=self_attn_mask,
                    self_attn_padding_mask=self_attn_padding_mask,
                    need_attn=bool((idx == alignment_layer)),
                    need_head_weights=bool((idx == alignment_layer)),
                )
            inner_states.append(x)
            if layer_attn is not None and idx == alignment_layer:
                attn = layer_attn.float().to(x)

        if attn is not None:
            if alignment_heads is not None:
                attn = attn[:alignment_heads]

            # average probabilities over heads
            attn = attn.mean(dim=0)

        if self.layer_norm is not None:
            x = self.layer_norm(x)

        # T x B x C -> B x T x C
        x = x.transpose(0, 1)

        if self.project_out_dim is not None:
            x = self.project_out_dim(x)

        return x, {"attn": [attn], "inner_states": inner_states}

    def output_layer(self, features, **kwargs):
        """Project features to the vocabulary size."""
        if self.adaptive_softmax is None:
            # project back to size of vocabulary
            return self.output_projection(features, **kwargs)
        else:
            return features

    def max_positions(self):
        """Maximum output length supported by the decoder."""
        if self.embed_positions is None:
            return self.max_target_positions
        return min(self.max_target_positions, self.embed_positions.max_positions)

    def buffered_future_mask(self, tensor):
        dim = tensor.size(0)
        # self._future_mask.device != tensor.device is not working in TorchScript. This is a workaround.
        if (
            self._future_mask.size(0) == 0
            or (not self._future_mask.device == tensor.device)
            or self._future_mask.size(0) < dim
        ):
            self._future_mask = torch.triu(
                utils.fill_with_neg_inf(torch.zeros([dim, dim])), 1
            )
        self._future_mask = self._future_mask.to(tensor)
        return self._future_mask[:dim, :dim]

    def upgrade_state_dict_named(self, state_dict, name):
        """Upgrade a (possibly old) state dict for new versions of fairseq."""
        if isinstance(self.embed_positions, SinusoidalPositionalEmbedding):
            weights_key = "{}.embed_positions.weights".format(name)
            if weights_key in state_dict:
                del state_dict[weights_key]
            state_dict["{}.embed_positions._float_tensor".format(name)] = (
                torch.FloatTensor(1)
            )

        if f"{name}.output_projection.weight" not in state_dict:
            if self.share_input_output_embed:
                embed_out_key = f"{name}.embed_tokens.weight"
            else:
                embed_out_key = f"{name}.embed_out"
            if embed_out_key in state_dict:
                state_dict[f"{name}.output_projection.weight"] = state_dict[
                    embed_out_key
                ]
                if not self.share_input_output_embed:
                    del state_dict[embed_out_key]

        for i in range(self.num_layers):
            # update layer norms
            layer_norm_map = {
                "0": "self_attn_layer_norm",
                "1": "encoder_attn_layer_norm",
                "2": "final_layer_norm",
            }
            for old, new in layer_norm_map.items():
                for m in ("weight", "bias"):
                    k = "{}.layers.{}.layer_norms.{}.{}".format(name, i, old, m)
                    if k in state_dict:
                        state_dict["{}.layers.{}.{}.{}".format(name, i, new, m)] = (
                            state_dict[k]
                        )
                        del state_dict[k]

        version_key = "{}.version".format(name)
        if utils.item(state_dict.get(version_key, torch.Tensor([1]))[0]) <= 2:
            # earlier checkpoints did not normalize after the stack of layers
            self.layer_norm = None
            self.normalize = False
            state_dict[version_key] = torch.Tensor([1])

        return state_dict

@register_model("linear_transformer_lm", dataclass=TransformerLanguageModelConfig)
class CasualTransformerLanguageModel(TransformerLanguageModel):
    @classmethod
    def add_args(cls, parser):
        super().add_args(parser)
        parser.add_argument('--gradient-checkpointing', type=lambda x: x.lower() == 'true', default=False)
        parser.add_argument('--gradient-checkpointing-every-n-layer', type=int, default=1)
        parser.add_argument('--gradient-checkpointing-layers',
                            type=lambda x: tuple([int(item) for item in x.split(',')]), default=None)


    @classmethod
    def build_model(cls, args, task):
        """Build a new model instance."""

        # make sure all arguments are present in older models
        base_lm_architecture(args)

        if args.decoder_layers_to_keep:
            args.decoder_layers = len(args.decoder_layers_to_keep.split(","))

        if getattr(args, "max_target_positions", None) is None:
            args.max_target_positions = getattr(
                args, "tokens_per_sample", DEFAULT_MAX_TARGET_POSITIONS
            )

        if args.character_embeddings:
            embed_tokens = CharacterTokenEmbedder(
                task.source_dictionary,
                eval(args.character_filters),
                args.character_embedding_dim,
                args.decoder_embed_dim,
                args.char_embedder_highway_layers,
            )
        elif args.adaptive_input:
            embed_tokens = AdaptiveInput(
                len(task.source_dictionary),
                task.source_dictionary.pad(),
                args.decoder_input_dim,
                args.adaptive_input_factor,
                args.decoder_embed_dim,
                options.eval_str_list(args.adaptive_input_cutoff, type=int),
                args.quant_noise_pq,
                args.quant_noise_pq_block_size,
            )
        else:
            embed_tokens = cls.build_embedding(
                args, task.source_dictionary, args.decoder_input_dim
            )

        if args.tie_adaptive_weights:
            assert args.adaptive_input
            assert args.adaptive_input_factor == args.adaptive_softmax_factor
            assert (
                args.adaptive_softmax_cutoff == args.adaptive_input_cutoff
            ), "{} != {}".format(
                args.adaptive_softmax_cutoff, args.adaptive_input_cutoff
            )
            assert args.decoder_input_dim == args.decoder_output_dim

        decoder = CasualTransformerDecoder(
            args, task.target_dictionary, embed_tokens, no_encoder_attn=True
        )
        return cls(decoder)

@register_model_architecture("linear_transformer_lm", "linear_transformer_lm_xl")
def large_linear_transformer_lm_architecture(args):
    if args.command_embed_dim is None:
        args.command_embed_dim = 128
    args.num_heads = getattr(args, "num_heads", 12)

    args.decoder_embed_dim = getattr(args, "decoder_embed_dim", 1024)
    args.decoder_ffn_embed_dim = getattr(args, "decoder_ffn_embed_dim", 4*1024)
    args.decoder_layers = getattr(args, "decoder_layers", 16)
    args.decoder_attention_heads = getattr(args, "decoder_attention_heads", 12)
    args.dropout = getattr(args, "dropout", 0.1)
    args.attention_dropout = getattr(args, "attention_dropout", 0.1)
    args.activation_fn = getattr(args, "activation_fn", "gelu")
    base_lm_architecture(args)

@register_task("language_modeling_control", dataclass=LanguageModelingConfig)
class LanguageModelingTaskWithControl(LanguageModelingTask):
    @classmethod
    def add_args(cls, parser):
        super().add_args(parser)
        parser.add_argument("--truncated_length", type=int, default=5868)

        parser.add_argument("--padding_to_max_length", type=int, default=0)
        parser.add_argument("--command_path", type=str)
        parser.add_argument("--command_embed_dim", type = int)
        parser.add_argument("--command_mask_prob", type=float, default=0.4)

        parser.add_argument("--is_inference", type = bool, default = False)
        print(parser)


    def load_dataset(self, split, epoch=1, combine=False, **kwargs):
        print("toi day")
        super().load_dataset(split, epoch=epoch, combine=combine, **kwargs)
        print("=============LOADED_DATASET================")

        command_dataset = np.load(f"data/truncated_2560/{split}_command.npy", allow_pickle=True)
        self.datasets[split] = CommandDataset(self.datasets[split], command_dataset, self.args)
        print(command_dataset)
        print(split)
        print(len(self.datasets[split]))
        print(split)
        print("split ne")
    def get_batch_iterator(
        self,
        dataset,
        max_tokens=None,
        max_sentences=None,
        max_positions=None,
        ignore_invalid_inputs=False,
        required_batch_size_multiple=1,
        seed=1,
        num_shards=1,
        shard_id=0,
        num_workers=0,
        epoch=1,
        data_buffer_size=0,
        disable_iterator_cache=False,
        skip_remainder_batch = False,grouped_shuffling=False, update_epoch_batch_itr=False
    ):
        print(f"====GET BATCH ITERATOR ======")
        split = None
        if 'train' in self.datasets and dataset == self.datasets['train']:
            split = 'train'
        elif 'valid' in self.datasets and dataset == self.datasets['valid']:
            split = 'valid'
        elif 'test' in self.datasets and dataset == self.datasets['test']:
            split = 'test'

        max_positions_split = getattr(self.args, 'max_positions_%s' % split, None)
        if max_positions_split is None:
            max_positions_split = getattr(self.args, 'truncate_%s' % split, None)
        if max_positions_split is not None:
            max_positions = max_positions_split
        print("=============GOT_BATCH================")
        return super().get_batch_iterator(
            dataset,
            max_tokens=max_tokens,
            max_sentences=max_sentences,
            max_positions=max_positions,
            ignore_invalid_inputs=ignore_invalid_inputs,
            required_batch_size_multiple=required_batch_size_multiple,
            seed=seed,
            num_shards=num_shards,
            shard_id=shard_id,
            num_workers=num_workers,
            epoch=epoch,
            data_buffer_size=data_buffer_size,
            disable_iterator_cache=disable_iterator_cache
        )
    def build_generator(
        self, models, args, seq_gen_cls=None, extra_gen_cls_kwargs=None
    ):
        print("=============BUILT_MODEL================")

        if getattr(args, "score_reference", False):
            from fairseq.sequence_scorer import SequenceScorer

            return SequenceScorer(
                self.target_dictionary,
                compute_alignment=getattr(args, "print_alignment", False),
            )

        from command_seq_generator import CommandSequenceGenerator
        print("HUUHUHUHUH")
        # Choose search strategy. Defaults to Beam Search.
        sampling = getattr(args, "sampling", False)
        sampling_topk = getattr(args, "sampling_topk", -1)
        sampling_topp = getattr(args, "sampling_topp", -1.0)
        diverse_beam_groups = getattr(args, "diverse_beam_groups", -1)
        diverse_beam_strength = getattr(args, "diverse_beam_strength", 0.5)
        match_source_len = getattr(args, "match_source_len", False)
        diversity_rate = getattr(args, "diversity_rate", -1)
        constrained = getattr(args, "constraints", False)
        prefix_allowed_tokens_fn = getattr(args, "prefix_allowed_tokens_fn", None)
        if (
            sum(
                int(cond)
                for cond in [
                    sampling,
                    diverse_beam_groups > 0,
                    match_source_len,
                    diversity_rate > 0,
                ]
            )
            > 1
        ):
            raise ValueError("Provided Search parameters are mutually exclusive.")
        assert sampling_topk < 0 or sampling, "--sampling-topk requires --sampling"
        assert sampling_topp < 0 or sampling, "--sampling-topp requires --sampling"

        if sampling:
            search_strategy = search.Sampling(
                self.target_dictionary, sampling_topk, sampling_topp
            )
        elif diverse_beam_groups > 0:
            search_strategy = search.DiverseBeamSearch(
                self.target_dictionary, diverse_beam_groups, diverse_beam_strength
            )
        elif match_source_len:
            # this is useful for tagging applications where the output
            # length should match the input length, so we hardcode the
            # length constraints for simplicity
            search_strategy = search.LengthConstrainedBeamSearch(
                self.target_dictionary,
                min_len_a=1,
                min_len_b=0,
                max_len_a=1,
                max_len_b=0,
            )
        elif diversity_rate > -1:
            search_strategy = search.DiverseSiblingsSearch(
                self.target_dictionary, diversity_rate
            )
        elif constrained:
            search_strategy = search.LexicallyConstrainedBeamSearch(
                self.target_dictionary, args.constraints
            )
        elif prefix_allowed_tokens_fn:
            search_strategy = search.PrefixConstrainedBeamSearch(
                self.target_dictionary, prefix_allowed_tokens_fn
            )
        else:
            search_strategy = search.BeamSearch(self.target_dictionary)

        if seq_gen_cls is None:
            if getattr(args, "print_alignment", False):
                raise ImportError("SequenceGeneratorWithAlignment is not allowed!")
                # seq_gen_cls = SequenceGeneratorWithAlignment
            else:
                seq_gen_cls = CommandSequenceGenerator
        extra_gen_cls_kwargs = extra_gen_cls_kwargs or {}
        return seq_gen_cls(
            models,
            self.target_dictionary,
            beam_size=getattr(args, "beam", 5),
            max_len_a=getattr(args, "max_len_a", 0),
            max_len_b=getattr(args, "max_len_b", 200),
            min_len=getattr(args, "min_len", 1),
            normalize_scores=(not getattr(args, "unnormalized", False)),
            len_penalty=getattr(args, "lenpen", 1),
            unk_penalty=getattr(args, "unkpen", 0),
            temperature=getattr(args, "temperature", 1.0),
            match_source_len=getattr(args, "match_source_len", False),
            no_repeat_ngram_size=getattr(args, "no_repeat_ngram_size", 0),
            search_strategy=search_strategy,
            **extra_gen_cls_kwargs,
        )





