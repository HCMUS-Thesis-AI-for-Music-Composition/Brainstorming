import os


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