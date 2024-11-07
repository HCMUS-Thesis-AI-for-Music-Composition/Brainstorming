import json
import re
import os
import subprocess
import sys

import platform as python_platform

class Platform:
    WINDOWS = "Windows"
    MACOS = "Darwin"

platform = python_platform.system()

windows_root_directory = "D:/Vector A/0. KHTN/Nam 4/HKII/Thesis/Brainstorming/DataCrawling"
mac_root_directory = "D:/Vector A/0. KHTN/Nam 4/HKII/Thesis/Brainstorming/DataCrawling"

root_directory = windows_root_directory if platform == Platform.WINDOWS else mac_root_directory

# sys.path.append(root_directory)

def open_edge_in_remote_debugging_mode(port, platform, browser_instance_data_dir):
    print(f"Opening Edge in remote debugging mode on port {port}...")

    macos_command = f'''open -na "Microsoft Edge.app" --args
                        --remote-debugging-port={port}
                        --user-data-dir="{browser_instance_data_dir}"'''

    windows_command = f'''start msedge.exe 
                        --remote-debugging-port={port} 
                        --user-data-dir="{browser_instance_data_dir}'''

    command = macos_command if platform == Platform.MACOS else windows_command
    
    os.system(command.replace("\n", " "))

def relative_to_absolute_path(relative_path, root_path):
    absolute_path = f"{root_path}/{relative_path}"
    return absolute_path

json_dir_path = relative_to_absolute_path(
    "GetAllSongHTML/song_list_link_by_artist/json",
    root_path=root_directory
)

def get_file_path_list_in_dir(dir_path):
    list_file_path = []
    for file_name in os.listdir(dir_path):
        file_path = f"{dir_path}/{file_name}"
        list_file_path.append(file_path)
    return list_file_path

def song_link_to_relative_html_file_path(link):
    artist_letter = link.split("/")[-2][0]
    artist = link.split("/")[-2]
    song = link.split("/")[-1]

    return f"{artist_letter}/{artist}/{song}.html"

# Ghi data vào file html
def write_data_to_html_file(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as html_file:
        html_file.write(data)

    print(f"-----> Data has been written to {file_name}")

# Đọc data từ file json
def read_data_from_json_file(file_name):
    with open(file_name, encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data

def windows_get_PID_of_process_running_on_port(port):
    command = f"netstat -a -n -o | findstr :{port}"

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    #   TCP    127.0.0.1:40000        0.0.0.0:0              LISTENING       6920
    regex_pattern = r"\s+TCP\s+127.0.0.1:\d+\s+\d+.\d+.\d+.\d+:\d+\s+LISTENING\s+(.+)"

    match = re.search(regex_pattern, result.stdout)

    pid = None

    if match:
        pid = match.group(1).replace(" ", "")
    else:
        pid = None

    return pid

def kill_process_running_on_port(port, platform=Platform.WINDOWS):
    print(f"Killing process running on port {port}...")

    try:
        if platform == Platform.MACOS:
            result = os.system(f"lsof -ti tcp:{port} | xargs kill -9")
        else:
            pid = windows_get_PID_of_process_running_on_port(port)

            if pid != None:
                result = subprocess.run(
                    f"taskkill /PID {pid} /F", 
                    shell=True, 
                    capture_output=True, 
                    text=True
                ).stdout
            else:
                result = f"No process is running on port {port}"
        print(result)
    except:
        print(f"Error when killing process running on port {port}")