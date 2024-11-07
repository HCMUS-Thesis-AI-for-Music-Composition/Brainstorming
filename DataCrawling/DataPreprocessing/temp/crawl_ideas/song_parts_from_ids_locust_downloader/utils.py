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

def read_song_id_of_song_parts_list(letter):
    '''
        Đọc danh sách các file json chứa thông tin về các bài hát từ thư mục song_id_of_song_parts theo chữ cái được truyền vào bằng tham số letter
    '''
    song_id_of_song_parts_list = []

    letter_dir = fu.relative_to_absolute_path(letter, song_ids_of_song_parts_dir)

    for artist in os.listdir(letter_dir):
        if (artist == ".DS_Store"):
            print(f"WARNING: skipped {artist} in {letter_dir}")
        else:
            artist_dir = fu.relative_to_absolute_path(artist, letter_dir)

            for song in os.listdir(artist_dir):
                absolute_song_file_path = fu.relative_to_absolute_path(song, artist_dir)
                
                song_id_of_song_parts_list.append(
                    fu.read_data_from_json_file(absolute_song_file_path)
                )

    return song_id_of_song_parts_list