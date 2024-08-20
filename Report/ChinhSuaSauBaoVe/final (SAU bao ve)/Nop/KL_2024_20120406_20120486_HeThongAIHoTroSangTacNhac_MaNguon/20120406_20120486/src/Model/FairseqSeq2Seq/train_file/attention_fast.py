from fast_transformers.attention.attention_layer import AttentionLayer

class CustomAttentionLayer(AttentionLayer):
    def __init__(self, attention, d_model, n_heads, d_keys=None, d_values=None):
        super(CustomAttentionLayer, self).__init__(attention, d_model, n_heads, d_keys, d_values)
        self.num_heads = n_heads
        self.num_dims = d_model
        self.head_dim = d_model // n_heads

    def forward(self, queries, keys, values, attn_mask=None, key_padding_mask=None, key_len = None):
        return super(CustomAttentionLayer, self).forward(queries, keys, values, attn_mask, key_padding_mask,key_len)
