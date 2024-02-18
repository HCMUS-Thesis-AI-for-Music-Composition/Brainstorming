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
                
                if os.path.exists(json_result_file_path) and os.path.getsize(json_result_file_path) > min_json_result_file_size:
                    print(f"SKIP: {json_result_file_path}")

                    skipped += 1
                    print(f"--------> TOTAL SKIPPED: {skipped}")
                    print()
                else:
                    song_id_of_song_parts_list.append(json_data)

    return song_id_of_song_parts_list