import platform as python_platform

class Platform:
    WINDOWS = "Windows"
    MACOS = "Darwin"

platform = python_platform.system()

windows_root_directory = "D:/Vector A/0. KHTN/Nam 4/HKII/Thesis/Brainstorming/DataCrawling"
mac_root_directory = "/Users/4rr311/Documents/VectorA/KHTN/Nam4/HKII/Thesis/Brainstorming/DataCrawling"

root_directory = windows_root_directory if platform == Platform.WINDOWS else mac_root_directory

import os
from os.path import join, getsize

import sys
sys.path.append(root_directory)

import os

import file_utils as fu

song_ids_of_song_parts_dir = fu.relative_to_absolute_path(
    "DataPreprocessing/song_id_of_song_parts",
    root_path=root_directory
)

song_parts_from_ids_dir = fu.relative_to_absolute_path(
    "DataPreprocessing/song_parts_from_ids",
    root_path=root_directory
)

http_status_code = fu.read_data_from_json_file(
    fu.relative_to_absolute_path(
        "http_status_code.json",
        root_directory
    )
)

# Chuyển status code từ string sang int
http_status_code = {int(k): v for k, v in http_status_code.items()}

def is_empty_main_data_existed(json_result_file_path):
    '''
        Kiểm tra xem file json kết quả có chứa empty main_data không
    '''
    result = False

    json_data = fu.read_data_from_json_file(json_result_file_path)

    if "song_parts" in json_data:
        for song_part in json_data["song_parts"]:
            if song_part["main_data"] is None or len(song_part["main_data"]) == 0:
                result = True
                break

    return result

def read_song_id_of_song_parts_list(letter, min_json_result_file_size = 10000):
    '''
        Đọc danh sách các file json chứa thông tin về các bài hát từ thư mục song_id_of_song_parts theo chữ cái được truyền vào bằng tham số letter. Nếu file đã tồn tại và file kết quả có size > min_json_result_file_size thì skip.
    '''
    song_id_of_song_parts_list = []

    letter_dir = fu.relative_to_absolute_path(letter, song_ids_of_song_parts_dir)

    skipped = 0

    for artist in os.listdir(letter_dir):
        if (artist == ".DS_Store"):
            print(f"WARNING: skipped {artist} in {letter_dir}")
        else:
            artist_dir = fu.relative_to_absolute_path(artist, letter_dir)

            for song in os.listdir(artist_dir):
                absolute_song_file_path = fu.relative_to_absolute_path(song, artist_dir)
                
                json_data = fu.read_data_from_json_file(absolute_song_file_path)

                song_link = json_data["link"]
                json_result_file_path = fu.song_link_to_relative_html_file_path(song_link)
                json_result_file_path = json_result_file_path.replace(".html", ".json")

                json_result_file_path = fu.relative_to_absolute_path(
                    relative_path = json_result_file_path,
                    root_path = song_parts_from_ids_dir
                )
                
                if os.path.exists(json_result_file_path) and os.path.getsize(json_result_file_path) > min_json_result_file_size and not is_empty_main_data_existed(json_result_file_path):
                    # print(f"SKIP: {json_result_file_path}")

                    skipped += 1
                    # print(f"--------> TOTAL SKIPPED: {skipped}")
                    # print()
                else:
                    if os.path.exists(json_result_file_path):
                        print(f"EXIST: {json_result_file_path}")
                        print(fu.read_data_from_json_file(json_result_file_path))
                    else:
                        print(f"NOT EXIST: {json_result_file_path}")

                    song_id_of_song_parts_list.append(json_data)

    return song_id_of_song_parts_list