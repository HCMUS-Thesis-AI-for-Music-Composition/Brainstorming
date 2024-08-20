from dataclasses import dataclass, field
from typing import Optional

from transformers import HfArgumentParser, TrainingArguments, set_seed
from transformers.trainer_utils import get_last_checkpoint
import json
import os
from transformers import (
    AutoTokenizer,
    BertConfig,
    BertTokenizer,
    BertTokenizerFast,
    DataCollatorWithPadding,
    EvalPrediction,
    HfArgumentParser,
    PretrainedConfig,
    Trainer,
    TrainingArguments,
    set_seed,
    EarlyStoppingCallback,
)


from transformers import TrainingArguments
from collections import OrderedDict


from copy import deepcopy
from mubert import BertForAttributModel

num_labels = json.load(open("num_labels.json", "r"))


def load_model(config_name="bert-large-uncased"):
    cache_dir = "./"
    config = BertConfig.from_pretrained(
        config_name,
        cache_dir=None,
        revision="main",
        use_auth_token=False,
    )
    tokenizer = AutoTokenizer.from_pretrained(
        config_name,
        cache_dir=None,
        use_fast=True,
        revision="main",
        use_auth_token=False,
    )
    model = BertForAttributModel.from_pretrained(
        config_name,
        config=config,
        tokenizer=tokenizer,
        cache_dir="./",
        revision="main",
        use_auth_token=False,
        ignore_mismatched_sizes=False,
        num_labels=num_labels,
    )
    model.tokenizer = tokenizer

    return config, tokenizer, model


# model_name = "bert-base-multilingual-uncased"
config, tokenizer, model = load_model("./tmp/checkpoint/checkpoint-2000")


def preprocess_function(examples, attributes, tokenizer, padding, max_seq_length):
    result = tokenizer(
        examples["text"], padding=padding, max_length=max_seq_length, truncation=True
    )
    if "labels" in examples:
        for idx in range(len(examples["labels"])):
            att_value = OrderedDict()
            for order, att in enumerate(attributes):
                att_value[att] = examples["labels"][idx][order].index(1)
            examples["labels"][idx] = deepcopy(att_value)
        result["labels"] = examples["labels"]
    return result


data_collator = DataCollatorWithPadding(tokenizer, pad_to_multiple_of=8)

trainer = Trainer(
    model=model,
    args=None,
    compute_metrics=None,
    tokenizer=tokenizer,
    data_collator=data_collator,
)
import pandas as pd
import datasets
import numpy as np
import torch

input_sentence = "Có đàn piano, không đàn guitar"


def tokenize_function(examples):
    return tokenizer(examples["text"], truncation=True)


from midi_data_extractor.attribute_unit import convert_value_dict_into_unit_dict

from midiprocessor import MidiEncoder


def mask_attributes(value_dict):
    random_pool = (
        list(range(1, 5)) * 5
        + list(range(6, 9)) * 3
        + list(range(9, len(value_dict.keys()))) * 2
    )
    chosen_num = np.random.choice(random_pool)
    chosen_attributes = np.random.choice(
        list(value_dict.keys()), chosen_num, replace=False
    )
    return chosen_attributes


def get_id(one_hot_vector):
    result = None
    for idx, item in enumerate(one_hot_vector):
        if item == 1:
            if result is not None:
                raise ValueError("This vector is not one-hot!")
            result = idx
    return result


def get_input_command_token_v3(command_dict, unit_dict):
    print(command_dict)
    print("-------------------")
    input_command_token = []
    key_order = [
        "I1s2",
        "I4",
        "C1",
        "R1",
        "R3",
        "S2s1",
        "S4",
        "B1s1",
        "TS1s1",
        "K1",
        "T1s1",
        "P4",
        "ST1",
        "EM1",
        "TM1",
    ]
    if -2 <= -1:
        chosen_keys = list(command_dict.keys())
        for key in key_order:

            if key == "I4":
                flag = False
                temp = command_dict["I1s2"]
                for i, ele in enumerate(temp):
                    if get_id(ele) == 0:
                        input_command_token.append(f"{key}_{i}")
                        flag = True
                        break
                if flag == False:
                    input_command_token.append(f"{key}_{len(temp)+1}")
            elif key == "C1":
                input_command_token.append(f"{key}_4")
            elif key == "ST1":
                input_command_token.append(f"{key}_14")
            else:
                cur_key_vector = command_dict[key]
                if key in chosen_keys:
                    if isinstance(cur_key_vector[0], int):
                        i = get_id(cur_key_vector)
                        input_command_token.append(f"{key}_{i}")
                    elif isinstance(cur_key_vector, (list, tuple)):

                        # i = get_id(list(cur_key_vector[0]))
                        # input_command_token.append(f"{key}_{i}")
                        if len(cur_key_vector) == 1:
                            i = get_id(cur_key_vector[0])
                            input_command_token.append(f"{key}_{i}")
                        else:
                            for ins, ele in enumerate(cur_key_vector):
                                i = get_id(ele)
                                input_command_token.append(f"{key}_{ins}_{i}")

                    else:
                        raise ValueError(
                            "cur_key_vector: %s   type: %s"
                            % (str(cur_key_vector), type(cur_key_vector))
                        )
                else:
                    if isinstance(cur_key_vector[0], int):  # 普通分类属性
                        i = (
                            len(cur_key_vector) - 1
                        )  # the last one always corresponds to NA
                        input_command_token.append(f"{key}_{i}")
                    elif isinstance(cur_key_vector[0], (list, tuple)):
                        for m, fine_vec in enumerate(cur_key_vector):
                            i = (
                                len(fine_vec) - 1
                            )  # the last one always corresponds to NA
                            input_command_token.append(f"{key}_{m}_{i}")
                    else:
                        raise ValueError(
                            "cur_key_vector: %s   type: %s"
                            % (str(cur_key_vector), type(cur_key_vector))
                        )
    return input_command_token


get_input_command_token = get_input_command_token_v3
midi_encoder = MidiEncoder("REMIGEN")


def to_command(values):
    unit_dict = convert_value_dict_into_unit_dict(values, midi_encoder)
    input_command_token = get_input_command_token(values, unit_dict)
    return input_command_token


att_key = json.load(open("att_key.json", "r"))


def stage2_prep(values):
    I1s2_key = []
    S4_key = []
    for att in att_key:
        if att[:4] == "I1s2":
            I1s2_key.append(att)
        if att[:2] == "S4":
            S4_key.append(att)
    pred_labels_I1s2 = []
    pred_labels_S4 = []
    for i1s2 in I1s2_key:
        pred_labels_I1s2.append(deepcopy(values[i1s2][0]))
        values.pop(i1s2)
    for s4 in S4_key:
        pred_labels_S4.append(deepcopy(values[s4][0]))
        values.pop(s4)
    values["I1s2"] = deepcopy(pred_labels_I1s2)
    values["S4"] = deepcopy(pred_labels_S4)
    return " ".join(to_command(values)) + " <sep>"
    print(to_command(values))


def infer_prompt(input_sentence):

    df = pd.DataFrame({"text": [input_sentence]})

    dataset = datasets.Dataset.from_pandas(df)
    tokenized_dataset = dataset.map(tokenize_function, batched=True)
    predictions = trainer.predict(
        tokenized_dataset, metric_key_prefix="predict"
    ).predictions
    result_output = {}
    print("----------------")
    predictions = predictions[1]
    print("---------------")
    for k, v in predictions.items():
        pred = np.argmax(predictions[k], axis=1)
        softmax = torch.nn.Softmax(dim=1)
        result_output[k] = np.zeros(predictions[k].shape, dtype=np.int8)
        for p in range(len(pred)):
            result_output[k][p, pred[p]] = 1
        result_output[k] = result_output[k].tolist()
    print(f"res {result_output}")
    return stage2_prep(result_output)
    # return to_command(result_output)


print(infer_prompt("có tiếng piano"))
