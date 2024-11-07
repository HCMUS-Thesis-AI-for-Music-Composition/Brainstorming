import math, os, warnings
from dataclasses import dataclass
from typing import List, Optional, Tuple, Union, Dict
from copy import deepcopy
from collections import OrderedDict

import torch
import torch.utils.checkpoint
from torch import nn
from torch.nn import BCEWithLogitsLoss, CrossEntropyLoss, MSELoss

from transformers.activations import ACT2FN
from transformers.modeling_outputs import (
    BaseModelOutputWithPoolingAndCrossAttentions,
)
from transformers.utils import (
    ModelOutput,
    logging,
)
from transformers import BertConfig
from transformers.models.bert.modeling_bert import (
    BertEmbeddings,
    BertSelfAttention,
    BertEncoder,
    BertPooler,
    BertAttention,
    BertPreTrainedModel,
    BertModel,
    BertLayer
)
class MuEmbeddings(BertEmbeddings):
  def __init__(self, config, num_labels, tokenizer):
    super().__init__(config)
    self.config = config
    self.num_labels = num_labels
    self.tokenizer = tokenizer
  def forward(
        self,
        input_ids: Optional[torch.LongTensor] = None,
        token_type_ids: Optional[torch.LongTensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        inputs_embeds: Optional[torch.FloatTensor] = None,
        past_key_values_length: int = 0,
    ) -> torch.Tensor:
        if input_ids is not None:
            input_shape = input_ids.size()
        else:
            input_shape = inputs_embeds.size()[:-1]

        seq_length = input_shape[1]

        if position_ids is None:
            position_ids = self.position_ids[:, past_key_values_length : seq_length + past_key_values_length]

        # Setting the token_type_ids to the registered buffer in constructor where it is all zeros, which usually occurs
        # when its auto-generated, registered buffer helps users when tracing the model without passing token_type_ids, solves
        # issue #5664
        if token_type_ids is None:
            if hasattr(self, "token_type_ids"):
                buffered_token_type_ids = self.token_type_ids[:, :seq_length]
                buffered_token_type_ids_expanded = buffered_token_type_ids.expand(input_shape[0], seq_length)
                token_type_ids = buffered_token_type_ids_expanded
            else:
                token_type_ids = torch.zeros(input_shape, dtype=torch.long, device=self.position_ids.device)

        if inputs_embeds is None:
            inputs_embeds = self.word_embeddings(input_ids)
        token_type_embeddings = self.token_type_embeddings(token_type_ids)

        embeddings = inputs_embeds + token_type_embeddings
        if self.position_embedding_type == "absolute":
            position_embeddings = self.position_embeddings(position_ids)
            embeddings += position_embeddings


        # Multi CLSes embeddings
        cls_tokens = [f"[unused{num}]" for num in range(len(self.num_labels))]
        cls_input_ids = self.tokenizer.convert_tokens_to_ids(cls_tokens)
        cls_input_ids = torch.tensor([cls_input_ids for _ in range(input_shape[0])]).to(token_type_ids.device)
        cls_token_type_ids = torch.zeros((input_shape[0], len(self.num_labels))).long().to(token_type_ids.device)
        cls_embeds = self.word_embeddings(cls_input_ids).to(token_type_ids.device)
        cls_token_type_embeddings = self.token_type_embeddings(cls_token_type_ids)
        cls_embeddings = cls_embeds + cls_token_type_embeddings

        embeddings = torch.cat((cls_embeddings, embeddings), dim=1)
        embeddings = self.LayerNorm(embeddings)
        embeddings = self.dropout(embeddings)
        return embeddings
class MusicBertSelfAttention(BertSelfAttention):
  def forward(
      self,
      hidden_states: torch.Tensor,
      attention_mask: Optional[torch.FloatTensor] = None,
      head_mask: Optional[torch.FloatTensor] = None,
      encoder_hidden_states: Optional[torch.FloatTensor] = None,
      encoder_attention_mask: Optional[torch.FloatTensor] = None,
      past_key_value: Optional[Tuple[Tuple[torch.FloatTensor]]] = None,
      output_attentions: Optional[bool] = False,
  ) -> Tuple[torch.Tensor]:
    return super().forward(hidden_states,
      attention_mask,
      head_mask,
      encoder_hidden_states,
      encoder_attention_mask,
      past_key_value,
      output_attentions)
class MusicBertAttention(BertAttention):
  def __init__(self, config, position_embedding_type=None):
      super().__init__(config, position_embedding_type)
      self.self = MusicBertSelfAttention(config, position_embedding_type=position_embedding_type)

class MusicBertLayer(BertLayer):
  def __init__(self, config):
      super().__init__(config)
      self.attention = MusicBertAttention(config)
      if self.add_cross_attention:
          if not self.is_decoder:
              raise ValueError(f"{self} should be used as a decoder model if cross attention is added")
          self.crossattention = MusicBertAttention(config, position_embedding_type="absolute")
class MusicBertEncoder(BertEncoder):
    def __init__(self, config):
        super().__init__(config)
        self.layer = nn.ModuleList([MusicBertLayer(config) for _ in range(config.num_hidden_layers)])
class MusicBertPooler(BertPooler):
    def forward(self, hidden_states: torch.Tensor, i: int) -> torch.Tensor:
        first_token_tensor = hidden_states[:, i]
        pooled_output = self.dense(first_token_tensor)
        pooled_output = self.activation(pooled_output)
        return pooled_output
class MusicBertModel(BertModel):
    def __init__(self, config, num_labels, tokenizer, add_pooling_layer=True):
        super().__init__(config)
        self.config = config
        self.num_labels = num_labels

        self.embeddings = MuEmbeddings(config, num_labels, tokenizer)
        self.encoder = MusicBertEncoder(config)

        self.pooler = MusicBertPooler(config) if add_pooling_layer else None

        # Initialize weights and apply final processing
        self.post_init()

    def forward(
        self,
        input_ids: Optional[torch.Tensor] = None,
        attention_mask: Optional[torch.Tensor] = None,
        token_type_ids: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.Tensor] = None,
        head_mask: Optional[torch.Tensor] = None,
        inputs_embeds: Optional[torch.Tensor] = None,
        encoder_hidden_states: Optional[torch.Tensor] = None,
        encoder_attention_mask: Optional[torch.Tensor] = None,
        past_key_values: Optional[List[torch.FloatTensor]] = None,
        use_cache: Optional[bool] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        return_dict: Optional[bool] = None,
    ) -> Union[Tuple[torch.Tensor], BaseModelOutputWithPoolingAndCrossAttentions]:
        output_attentions = output_attentions if output_attentions is not None else self.config.output_attentions
        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        if self.config.is_decoder:
            use_cache = use_cache if use_cache is not None else self.config.use_cache
        else:
            use_cache = False

        if input_ids is not None and inputs_embeds is not None:
            raise ValueError("You cannot specify both input_ids and inputs_embeds at the same time")
        elif input_ids is not None:
            input_shape = input_ids.size()
        elif inputs_embeds is not None:
            input_shape = inputs_embeds.size()[:-1]
        else:
            raise ValueError("You have to specify either input_ids or inputs_embeds")

        batch_size, seq_length = input_shape
        device = input_ids.device if input_ids is not None else inputs_embeds.device

        # past_key_values_length
        past_key_values_length = past_key_values[0][0].shape[2] if past_key_values is not None else 0

        if attention_mask is None:
            attention_mask = torch.ones(((batch_size, seq_length + past_key_values_length)), device=device)

        if token_type_ids is None:
            if hasattr(self.embeddings, "token_type_ids"):
                buffered_token_type_ids = self.embeddings.token_type_ids[:, :seq_length]
                buffered_token_type_ids_expanded = buffered_token_type_ids.expand(batch_size, seq_length)
                token_type_ids = buffered_token_type_ids_expanded
            else:
                token_type_ids = torch.zeros(input_shape, dtype=torch.long, device=device)

        # We can provide a self-attention mask of dimensions [batch_size, from_seq_length, to_seq_length]
        # ourselves in which case we just need to make it broadcastable to all heads.
        #????
        cls_attention_mask = torch.tensor([[1 for _ in range(len(self.num_labels))] for _ in range(input_shape[0])]).long().to(attention_mask.device)
        attention_mask = torch.cat((cls_attention_mask, attention_mask), dim=1)
        extended_attention_mask: torch.Tensor = self.get_extended_attention_mask(attention_mask, input_shape)

        # If a 2D or 3D attention mask is provided for the cross-attention
        # we need to make broadcastable to [batch_size, num_heads, seq_length, seq_length]
        if self.config.is_decoder and encoder_hidden_states is not None:
            encoder_batch_size, encoder_sequence_length, _ = encoder_hidden_states.size()
            encoder_hidden_shape = (encoder_batch_size, encoder_sequence_length)
            if encoder_attention_mask is None:
                encoder_attention_mask = torch.ones(encoder_hidden_shape, device=device)
            encoder_extended_attention_mask = self.invert_attention_mask(encoder_attention_mask)
        else:
            encoder_extended_attention_mask = None

        # Prepare head mask if needed
        # 1.0 in head_mask indicate we keep the head
        # attention_probs has shape bsz x n_heads x N x N
        # input head_mask has shape [num_heads] or [num_hidden_layers x num_heads]
        # and head_mask is converted to shape [num_hidden_layers x batch x num_heads x seq_length x seq_length]
        head_mask = self.get_head_mask(head_mask, self.config.num_hidden_layers)

        embedding_output = self.embeddings(
            input_ids=input_ids,
            position_ids=position_ids,
            token_type_ids=token_type_ids,
            inputs_embeds=inputs_embeds,
            past_key_values_length=past_key_values_length,
        )
        encoder_outputs = self.encoder(
            embedding_output,
            attention_mask=extended_attention_mask,
            head_mask=head_mask,
            encoder_hidden_states=encoder_hidden_states,
            encoder_attention_mask=encoder_extended_attention_mask,
            past_key_values=past_key_values,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
        )
        sequence_output = encoder_outputs[0]
        pooled_output = self.pooler(sequence_output,0) if self.pooler is not None else None

        if not return_dict:
            return (sequence_output, pooled_output) + encoder_outputs[1:]

        return BaseModelOutputWithPoolingAndCrossAttentions(
            last_hidden_state=sequence_output,                      # Sequence of hidden-states at the output of the last layer of the model
            pooler_output=pooled_output,                            # [CLS]
            past_key_values=encoder_outputs.past_key_values,
            hidden_states=encoder_outputs.hidden_states,            # Tuple of torch.FloatTensor (one for the output of the embeddings, if the model has an embedding layer, + one for the output of each layer) of shape (batch_size, sequence_length, hidden_size)
            attentions=encoder_outputs.attentions,
            cross_attentions=encoder_outputs.cross_attentions,
        )




@dataclass
class SequenceClassifierOutputForMultiTask(ModelOutput):
    loss: Optional[torch.FloatTensor] = None
    logits: Dict[str, any] = None
    hidden_states: Optional[Tuple[torch.FloatTensor]] = None
    attentions: Optional[Tuple[torch.FloatTensor]] = None

class BertForAttributModel(BertPreTrainedModel):
    def __init__(self, config, num_labels, tokenizer):
        super().__init__(config)
        self.num_labels = num_labels
        self.config = config
        self.tokenizer = tokenizer

        self.bert = MusicBertModel(config, num_labels, tokenizer)
        self.pooler = MusicBertPooler(config)
        classifier_dropout = (
            config.classifier_dropout if config.classifier_dropout is not None else config.hidden_dropout_prob
        )
        self.dropout = nn.Dropout(classifier_dropout)

        self.classifieratt = nn.ModuleList([nn.Linear(config.hidden_size, v) for v in self.num_labels.values()])

        # Initialize weights and apply final processing
        self.post_init()
    def forward(
        self,
        input_ids: Optional[torch.Tensor] = None,
        attention_mask: Optional[torch.Tensor] = None,
        token_type_ids: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.Tensor] = None,
        head_mask: Optional[torch.Tensor] = None,
        inputs_embeds: Optional[torch.Tensor] = None,
        labels: Optional[torch.Tensor] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        return_dict: Optional[bool] = None,
    ) -> Union[Tuple[torch.Tensor], SequenceClassifierOutputForMultiTask]:
        r"""
        labels (`torch.LongTensor` of shape `(batch_size,)`, *optional*):
            Labels for computing the sequence classification/regression loss. Indices should be in `[0, ...,
            config.num_labels - 1]`. If `config.num_labels == 1` a regression loss is computed (Mean-Square loss), If
            `config.num_labels > 1` a classification loss is computed (Cross-Entropy).
        """
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        outputs = self.bert(
            input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            position_ids=position_ids,
            head_mask=head_mask,
            inputs_embeds=inputs_embeds,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
        )

        sequence_output = outputs['last_hidden_state']                  # last hidden states
        pooled_outputs = OrderedDict()
        logits = OrderedDict()
        i = 0
        for idx, k in enumerate(self.num_labels.keys()):
            assert self.num_labels[k] == self.classifieratt[idx].out_features
            pooled_outputs[k] = self.pooler(sequence_output, i)
            i += 1
            logits[k] = self.classifieratt[idx](self.dropout(pooled_outputs[k]))

        total_loss = torch.tensor(0.0).to(input_ids.device)
        loss = {}
        if labels is not None:
            for k in labels.keys():
                loss_fct = CrossEntropyLoss()
                loss[k] = loss_fct(logits[k].view(-1, self.num_labels[k]), labels[k].view(-1))
                total_loss += loss[k]

        if not return_dict:
            output = (logits,) + outputs[2:]
            return ((total_loss,) + output) if total_loss is not None else output

        return SequenceClassifierOutputForMultiTask(
            loss = total_loss,
            logits = logits,
            hidden_states=outputs.hidden_states,
            attentions=outputs.attentions,
        )