'''
MÔI TRƯỜNG THỰC THI:

- MacOS Sonoma 14.0
- CPU Apple M1
- Trình duyệt Microsoft Edge Version 118.0.2088.76 (Official build) (arm64)
- Python 3.10.10
- locust 2.18.0 (cài đặt với pip)
- selenium 4.14.0 (cài đặt với pip)

'''

import random
from locust import User, SequentialTaskSet, task
from locust.event import EventHook

from selenium import webdriver

import platform as python_platform
import time
import os

import selenium_utils
import utils

#######

# import sys

# class Platform:
#     WINDOWS = "Windows"
#     MACOS = "Darwin"

# platform = python_platform.system()

# windows_root_directory = "D:/Vector A/0. KHTN/Nam 4/HKII/Thesis/Brainstorming/DataCrawling"
# mac_root_directory = "D:/Vector A/0. KHTN/Nam 4/HKII/Thesis/Brainstorming/DataCrawling"

# root_directory = windows_root_directory if platform == Platform.WINDOWS else mac_root_directory

# sys.path.append(root_directory)

#######

song_group_letter = "a"

logging_event_hook = EventHook()

port_manager_event_hook = EventHook()

get_used_ports_event_hook = EventHook()

class SequentialSeleniumTasks(SequentialTaskSet):
    browser_instance_data_dir = None
    free_port = None

    browser = None
    url = None

    @task
    def init(self):
        song_links_by_alphabet = utils.get_file_path_list_in_dir(utils.json_dir_path)

        song_links_by_alphabet = {
            path.split("/")[-1].split(".")[0].lower() : path
            for path in song_links_by_alphabet
        }
        song_links = utils.read_data_from_json_file(song_links_by_alphabet[song_group_letter])

        # Xóa các song đã được crawl
        song_links = [song for song in song_links
            if not os.path.exists(
                utils.relative_to_absolute_path(
                    utils.song_link_to_relative_html_file_path(song["link"]),
                    root_path=utils.relative_to_absolute_path(
                        "GetAllSongHTML/song_list/raw_html",
                        root_path=utils.root_directory
                    )
                )
            )
        ]

        # Lấy link của bài hát ngẫu nhiên
        self.url = song_links[random.randint(0, len(song_links) - 1)]["link"]
        
        port_to_run_browser = 40000

        used_ports = get_used_ports_event_hook.fire()

        while port_to_run_browser in used_ports:
            port_to_run_browser += 1

        port_manager_event_hook.fire(
            port = port_to_run_browser,
            should_release = False
        ) 

        self.free_port = port_to_run_browser

        
    @task
    def open_remote_debugging_edge(self):
        '''
            Mở Edge ở chế độ Remote Debugging
        '''
        
        self.browser_instance_data_dir = \
            f"{utils.root_directory}/GetAllSongHTML/song_list/browser_instance_data/{self.free_port}"

        print(f"Opening remote debugging edge at port {self.free_port}")

        # Mở Edge ở chế độ Remote Debugging với port được cấp
        utils.open_edge_in_remote_debugging_mode(
            self.free_port,
            utils.platform,
            self.browser_instance_data_dir
        )

    @task
    def init_selenium_instance(self):
        print(f"Initializing Selenium browser instance with port {self.free_port}")
    
        # Kết nối Selenium đến Edge ở port được mở
        options = webdriver.EdgeOptions()
        options.add_experimental_option("debuggerAddress", f"localhost:{self.free_port}")
        
        self.browser = webdriver.Edge(options=options)
    
    @task
    def get_raw_html(self):
        start_time = time.time()

        is_success = True

        try:
            selenium_utils.get_song_raw_html(self.url, self.browser)
            is_success = True
        except:
            print(f"Failed to get {self.url}")
            is_success = False

        end_time = time.time()

        response_time = (end_time - start_time) * 1000
        response_time = int(response_time)


        html_path = utils.relative_to_absolute_path(
            utils.song_link_to_relative_html_file_path(self.url),
            root_path=utils.relative_to_absolute_path(
                "GetAllSongHTML/song_list/raw_html",
                root_path=utils.root_directory
            )
        )

        # Tính response time và kích thước của file html
        response_time = response_time if is_success else 0
        content_length = os.path.getsize(html_path) if is_success else 0

        logging_event_hook.fire(
            method = "Selenium",
            name = "Get raw HTML",
            content_length = content_length, # Ở HttpUser là kích thước của các response (đơn vị byte)
            response_time = response_time
        )

    @task
    def after_running(self):
        try:
            utils.kill_process_running_on_port(self.free_port, utils.platform)

            # Get handles of all open tabs
            handles = self.browser.window_handles

            # Iterate through handles and close tabs
            for handle in handles:
                self.browser.switch_to.window(handle)
                self.browser.close()

            # Quit the browser
            self.browser.quit()

            # Release the port
            port_manager_event_hook.fire(
                port = self.free_port,
                should_release = True
            ) 
        except Exception as e:
            print(f"Error when closing browser: {e}")
        

    def on_stop(self):
        try:
            utils.kill_process_running_on_port(self.free_port, utils.platform)
            if python_platform.system() == "Windows":
                os.system("taskkill /F /IM msedge.exe")
                os.system("taskkill /F /IM msedgedriver.exe")
        except Exception as e:
            print(f"Error when closing browser (on stop): {e}")

class MyUser(User):
    tasks = [SequentialSeleniumTasks]
    used_ports = []

    def logging_event_handler(self, method, name, content_length, response_time):

        print(f"Event was fired with arguments: {method}, {name}")

        self.environment.runner.stats.log_request(
            method=method,
            content_length=content_length,
            name=name, 
            response_time=response_time
        )

    def port_manager_handler(self, port, should_release):
        if should_release:
            self.used_ports.remove(port)
        else:
            self.used_ports.append(port)

    def get_used_ports_handler(self):
        return self.used_ports

    def on_start(self):
        logging_event_hook.add_listener(self.logging_event_handler)
        port_manager_event_hook.add_listener(self.port_manager_handler)
        get_used_ports_event_hook.add_listener(self.get_used_ports_handler)