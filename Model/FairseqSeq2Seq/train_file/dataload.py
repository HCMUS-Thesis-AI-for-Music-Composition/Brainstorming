import torch
from torch.utils.data import Dataset, DataLoader
from midiprocessor import MidiEncoder
import numpy as np
from midi_data_extractor.attribute_unit import convert_value_dict_into_unit_dict
from fairseq.data.base_wrapper_dataset import BaseWrapperDataset
from fairseq.data import data_utils

def mask_attributes(value_dict):
    random_pool = list(range(1, 5))*5 + list(range(6, 9))*3 + list(range(9, len(value_dict.keys())))*2
    chosen_num = np.random.choice(random_pool)
    chosen_attributes = np.random.choice(list(value_dict.keys()), chosen_num, replace=False)
    return chosen_attributes


def get_id(one_hot_vector):
    result = None
    for idx, item in enumerate(one_hot_vector):
        if item == 1:
            if result is not None:
                raise ValueError("This vector is not one-hot!")
            result = idx
    return result
def get_input_command_token_v3(dataset, command_dict, unit_dict):
    input_command_token = []
    #if dataset.args.command_mask_prob <= -1:
    if -2<= -1:
        chosen_keys = mask_attributes(command_dict["values"])
        for key in dataset.key_order:
            cur_key_vector = unit_dict[key].get_vector(use=True)

            if key in chosen_keys:
                if isinstance(cur_key_vector[0], int):  # 普通分类属性
                    i = get_id(cur_key_vector)
                    input_command_token.append(f"{key}_{i}")
                elif isinstance(cur_key_vector[0], (list, tuple)):
                    true_pos = []
                    NA_pos = []
                    for i in range(len(cur_key_vector)):
                        if cur_key_vector[i][0] == 1:
                            true_pos.append(i)
                        else:
                            NA_pos.append(i)
                    # if len(true_pos) <= 0:
                    #     # for S4, no genre label
                    #     assert key == "S4", f"error true pos for {key} of {index}!"
                    chosen_num = np.random.randint(min(1, len(true_pos)),
                                                   len(true_pos) + 1)  # choose 1 pos at least
                    chosen_true_pos = np.random.choice(true_pos, chosen_num, replace=False)

                    chosen_num = np.random.randint(min(1, len(NA_pos)), len(NA_pos) + 1)
                    chosen_false_pos = np.random.choice(NA_pos, chosen_num, replace=False)
                    for m, fine_vec in enumerate(cur_key_vector):
                        if m in chosen_true_pos:
                            i = get_id(fine_vec) # yes
                        elif m in chosen_false_pos:
                            i = len(fine_vec) - 2 # yes, no, NA --- 0,1,2
                        else:
                            i = len(fine_vec) - 1  # This attribute is not chosen or is NA, set to NA token
                        input_command_token.append(f"{key}_{m}_{i}")
                else:
                    raise ValueError("cur_key_vector: %s   type: %s" % (str(cur_key_vector), type(cur_key_vector)))
            else:
                if isinstance(cur_key_vector[0], int):  # 普通分类属性
                    i = len(cur_key_vector) - 1  # the last one always corresponds to NA
                    input_command_token.append(f"{key}_{i}")
                elif isinstance(cur_key_vector[0], (list, tuple)):
                    for m, fine_vec in enumerate(cur_key_vector):
                        i = len(fine_vec) - 1  # the last one always corresponds to NA
                        input_command_token.append(f"{key}_{m}_{i}")
                else:
                    raise ValueError("cur_key_vector: %s   type: %s" % (str(cur_key_vector), type(cur_key_vector)))
    else:
        for key in dataset.key_order:
            cur_key_vector = unit_dict[key].get_vector(use=True)
            if isinstance(cur_key_vector[0], int):  # 普通分类属性
                if np.random.rand() < 0.4:#dataset.args.command_mask_prob:
                    i = len(cur_key_vector) - 1  # the last one always corresponds to NA
                else:
                    i = get_id(cur_key_vector)
                input_command_token.append(f"{key}_{i}")
            elif isinstance(cur_key_vector[0], (list, tuple)):
                for m, fine_vec in enumerate(cur_key_vector):
                    if np.random.rand() < -1:#dataset.args.command_mask_prob:
                        i = len(fine_vec) - 1  # the last one always corresponds to NA
                    else:
                        i = get_id(fine_vec)
                    input_command_token.append(f"{key}_{m}_{i}")
            else:
                raise ValueError("cur_key_vector: %s   type: %s" % (str(cur_key_vector), type(cur_key_vector)))
    return input_command_token

class CommandDataset(BaseWrapperDataset):
  def __init__(self, dataset, command_data, args = None):
    super().__init__(dataset)

    self.command_data = command_data
    self.args = args
    self._sizes = self.dataset.sizes.copy()

    self.command_length_step = []
    self.midi_encoder = MidiEncoder("REMIGEN")
    self.pad_token_id = self.dataset.vocab.pad()
    self.sep_token_id = self.dataset.vocab.index("<sep>")
    self.key_order = ['I1s2', 'I4', 'C1', 'R1', 'R3', 'S2s1', 'S4', 'B1s1', 'TS1s1', 'K1', 'T1s1', 'P4', 'ST1', 'EM1', 'TM1']
    self.key_has_NA = []
    self.multi_hot_attributes = ["I1s2", "S4"]
    self.get_input_command_token = get_input_command_token_v3
    self.key_index = dict(zip(self.key_order, range(len(self.key_order))))
  def __len__(self):
    return len(self.dataset)
  def __getitem__(self, index):
        sample = self.dataset[index]
        command_dict = self.command_data[index]
        truncated_length = 2560
        print(sample["source"])
        print("---------------")
        for ele in sample["source"][:5]:
          print(self.dataset.vocab[ele])    
        print(self.dataset.vocab[6])    
        if len(sample["source"]) > truncated_length + 2:
            if 1!=1:#self.args.padding_to_max_length:
                raise ValueError(f"Sample length is greater than {self.args.truncated_length}!")
            else:
                sample["source"] = sample["source"][:truncated_length]
                sample["target"] = sample["target"][:truncated_length]

        unit_dict = convert_value_dict_into_unit_dict(command_dict["values"], self.midi_encoder)

        input_command_token = self.get_input_command_token(self, command_dict, unit_dict)
        input_command = []
        for word in input_command_token:
            input_command.append(self.dataset.tgt_vocab.index(word))
        input_command.append(self.sep_token_id)
        input_command = torch.tensor(input_command, dtype=torch.int64)
        print(sample)
        print("sample source 0 1")
        print(sample["source"][0:1])
        sample["source"] = torch.cat([sample["source"][0:1], input_command, sample["source"][1:]], dim=0)
        pad_vector = torch.tensor(np.zeros(len(input_command)).astype(np.int64) + self.pad_token_id).to(sample["target"].device)
        sample["target"] = torch.cat([pad_vector, sample["target"]], dim=0)

        if 1:#self.args.padding_to_max_length:
            if len(sample["source"]) < truncated_length:
                pad_vector = torch.tensor(np.zeros(truncated_length + 2 - len(sample["source"])).astype(np.int64) + self.pad_token_id).to(sample["target"].device)
                sample["source"] = torch.cat([sample["source"], pad_vector], dim=0)
                sample["target"] = torch.cat([sample["target"], pad_vector], dim=0)

        print(len(input_command))
        print("input command")
        print(list(sample["source"]))
        print("==========")
        print((list(sample["target"])))
        print("----TARGET-----")
        print(index)
        print("---------over----------")
        print(len(input_command))
        return {
            "id": index,
            "source": sample["source"],
            "target": sample["target"],
            "sep_pos": len(input_command)
        }
  def dynamic_mask(self, command_input):
        # random set N/A for command_input
        return command_input

  @property
  def sizes(self):
      return self._sizes

  def size(self, index):
      return self._sizes[index]

  def num_tokens(self, index):
      return self._sizes[index]

  def filter_indices_by_size(self, indices, max_sizes):
      """
      Filter a list of sample indices. Remove those that are longer than
      specified in *max_sizes*.

      WARNING: don't update, override method in child classes

      Args:
          indices (np.array): original array of sample indices
          max_sizes (int or list[int] or tuple[int]): max sample size,
              can be defined separately for src and tgt (then list or tuple)

      Returns:
          np.array: filtered sample array
          list: list of removed indices
      """
      if isinstance(max_sizes, float) or isinstance(max_sizes, int):
          if hasattr(self, "sizes") and isinstance(self.sizes, np.ndarray):
              ignored = indices[self.sizes[indices] > max_sizes].tolist()
              indices = indices[self.sizes[indices] <= max_sizes]
          elif (
              hasattr(self, "sizes")
              and isinstance(self.sizes, list)
              and len(self.sizes) == 1
          ):
              ignored = indices[self.sizes[0][indices] > max_sizes].tolist()
              indices = indices[self.sizes[0][indices] <= max_sizes]
          else:
              indices, ignored = data_utils._filter_by_size_dynamic(
                  indices, self.size, max_sizes
              )
      else:
          indices, ignored = data_utils._filter_by_size_dynamic(
              indices, self.size, max_sizes
          )
      if len(ignored) > 0:
          print(self.sizes)
          print(ignored)
          print(max_sizes)
      return indices, ignored

  def collater(self, samples):
      # samples: list->dict, just as __get_item__(index) rets
      # print("samples type:", type(samples))

      return self.collate_helper(samples, self.dataset.vocab.pad(), self.dataset.vocab.eos())
  def collate_helper(self, samples, pad_idx, eos_idx):
      if len(samples) == 0:
          return {}
      def merge(key, is_list=False):
          if is_list:
              res = []
              for i in range(len(samples[0][key])):
                  res.append(
                      data_utils.collate_tokens(
                          [s[key][i] for s in samples],
                          pad_idx,
                          eos_idx,
                          left_pad=False,
                      )
                  )
              return res
          else:
              return data_utils.collate_tokens(
                  [s[key] for s in samples],
                  pad_idx,
                  eos_idx,
                  left_pad=False,
              )

      src_tokens = merge("source")
      if samples[0]["sep_pos"] is not None:
          sep_pos = [samples[j]["sep_pos"] for j in range(len(samples))]
      else:
          sep_pos = None
      if samples[0]["target"] is not None:
          is_target_list = isinstance(samples[0]["target"], list)
          target = merge("target", is_target_list)
      else:
          target = src_tokens

      return {
          "id": torch.LongTensor([s["id"] for s in samples]),
          "nsentences": len(samples),
          "ntokens": sum(len(s["source"]) for s in samples),
          "net_input": {
              "src_tokens": src_tokens,
              "sep_pos": sep_pos,
              "src_lengths": torch.LongTensor([s["source"].numel() for s in samples]),
          },
          "target": target,
      }
