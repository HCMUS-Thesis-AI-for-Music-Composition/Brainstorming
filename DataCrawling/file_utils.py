import os
import json


def relative_to_absolute_path(relative_path, root_path):
    absolute_path = f"{root_path}/{relative_path}"
    return absolute_path

# Lấy danh sách đường dẫn đến các file trong thư mục (không đệ quy)
def get_file_path_list_in_dir(dir_path):
    list_file_path = []
    for file_name in os.listdir(dir_path):
        file_path = f"{dir_path}/{file_name}"
        list_file_path.append(file_path)
    return list_file_path

# Đọc data từ file json
def read_data_from_json_file(file_name):
    with open(file_name, encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data

# Ghi data vào file json
def write_data_to_json_file(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

# Ghi data vào file html
def write_data_to_html_file(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as html_file:
        html_file.write(data)

# Append to json file
def append_data_to_json_file(data, file_name):
    with open(file_name, 'r+', encoding='utf-8') as json_file:
        old_data = json.load(json_file)
        old_data.append(data)
        json_file.seek(0)
        json.dump(old_data, json_file, ensure_ascii=False, indent=4)
        json_file.truncate()