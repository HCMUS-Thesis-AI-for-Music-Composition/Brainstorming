'''
MÔI TRƯỜNG THỰC THI:

- MacOS Sonoma 14.0
- CPU Apple M1
- Trình duyệt Microsoft Edge Version 118.0.2088.76 (Official build) (arm64)
- Python 3.10.10
- locust 2.18.0 (cài đặt với pip)
- selenium 4.14.0 (cài đặt với pip)

'''

import json
import shutil
from locust import User, SequentialTaskSet, task, between
from locust.event import EventHook

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import datetime
import time
import os

import selenium_utils
import utils

logging_event_hook = EventHook()

test_datetime = utils.current_datetime()

class SequentialSeleniumTasks(SequentialTaskSet):
    init_time = None

    browser_instance_data_dir = None
    free_port = None

    browser = None

    report_dir = ""

    @task
    def init(self):
        self.init_time = utils.current_datetime()

        self.report_dir = f"{utils.report_folder}/{test_datetime.replace('/', ' ').replace(':', ' ')}"
        
        # Code tạo custom report
        # # Tạo thư mục report_dir nếu chưa tồn tại trên máy
        # if not os.path.exists(self.report_dir):
        #     os.makedirs(self.report_dir)

        # # Tạo file created test cases nếu chưa tồn tại trên máy
        # if not os.path.exists(f"{self.report_dir}/created_test_cases.json"):
        #     os.system(f'touch "{self.report_dir}/created_test_cases.json"')
            
        #     # Append một mảng rỗng vào file json
        #     with open(f"{self.report_dir}/created_test_cases.json", 'w') as file:
        #         json.dump([], file)

        # # Append dữ liệu vào file created test cases
        # with open(f"{self.report_dir}/created_test_cases.json", 'w') as file:
        #     created_test_cases = json.load(file)
        #     created_test_cases.append({
        #         "Time": self.init_time,
        #         "Name": selenium_utils.create_asset_account_name(self.init_time)
        #     })

        # # Tạo file success test cases nếu chưa tồn tại trên máy
        # if not os.path.exists(f"{self.report_dir}/success_test_cases.json"):
        #     os.system(f'touch "{self.report_dir}/success_test_cases.json"')
            
        #     # Append một mảng rỗng vào file json
        #     with open(f"{self.report_dir}/success_test_cases.json", 'w') as file:
        #         json.dump([], file)

        # # Tạo file failed test cases nếu chưa tồn tại trên máy
        # if not os.path.exists(f"{self.report_dir}/failed_test_cases.json"):
        #     os.system(f'touch "{self.report_dir}/failed_test_cases.json"')
            
        #     # Append một mảng rỗng vào file json
        #     with open(f"{self.report_dir}/failed_test_cases.json", 'w') as file:
        #         json.dump([], file)

    @task
    def open_remote_debugging_edge(self):
        '''
            Mở Edge ở chế độ Remote Debugging
        '''
        
        # Tìm một port trống để chạy browser instance
        self.free_port, socket = utils.find_free_port()

        reformatted_datetime = self.init_time.replace('/', ' ').replace(':', ' ')
        # Chọn thư mục lưu dữ liệu của browser instance
        self.browser_instance_data_dir = \
            f"{utils.browser_instance_data_dir}/{reformatted_datetime} {self.free_port}"

        print(f"Opening remote debugging edge at port {self.free_port}")

        # Mở Edge ở chế độ Remote Debugging với port được cấp
        remote_debugging_command = f'''open -na "Microsoft Edge.app" --args
            --remote-debugging-port={self.free_port}
            --user-data-dir="{self.browser_instance_data_dir}"
        '''
        
        socket.close()
        os.system(remote_debugging_command.replace("\n", " "))


    @task
    def init_selenium_instance(self):
        print(f"Initializing Selenium browser instance with port {self.free_port}")
    
        # Kết nối Selenium đến Edge ở port được mở
        options = webdriver.EdgeOptions()
        options.add_experimental_option("debuggerAddress", f"localhost:{self.free_port}")
        options.add_argument("--incognito")  
        # options.add_argument("headless")

        self.browser = webdriver.Edge(options=options)
    
    @task
    def go_to_login_page(self):
        '''
            Truy cập vào trang đăng nhập
        '''
        start_time = time.time()

        selenium_utils.go_to_login_page(self.browser)

        end_time = time.time()

        response_time = (end_time - start_time) * 1000
        response_time = int(response_time)

        logging_event_hook.fire(
            method = "Selenium",
            name = "Open Login page",
            content_length = 0, # Ở HttpUser là kích thước của các response (đơn vị byte)
            response_time = response_time
        )

    @task
    def enter_email_and_password(self):
        '''
            Nhập email và password vào trang đăng nhập
        '''
        start_time = time.time()

        selenium_utils.enter_email_and_password(self.browser, utils.email, utils.password)

        end_time = time.time()

        response_time = (end_time - start_time) * 1000
        response_time = int(response_time)

        logging_event_hook.fire(
            method = "Selenium",
            name = "Enter email and password",
            content_length = 0, # Ở HttpUser là kích thước của các response (đơn vị byte)
            response_time = response_time
        )

    @task
    def go_to_create_asset_account_page(self):
        '''
            Đi đến trang tạo Asset Account
        '''
        start_time = time.time()

        selenium_utils.go_to_create_asset_account_page(self.browser)

        end_time = time.time()

        response_time = (end_time - start_time) * 1000
        response_time = int(response_time)

        logging_event_hook.fire(
            method = "Selenium",
            name = "Open Create Asset Account page",
            content_length = 0, # Ở HttpUser là kích thước của các response (đơn vị byte)
            response_time = response_time
        )

    @task
    def enter_asset_account_name(self):
        '''
            Nhập tên Asset Account
        '''
        start_time = time.time()

        selenium_utils.enter_asset_account_name(
            self.browser, 
            selenium_utils.create_asset_account_name(self.init_time)
        )

        end_time = time.time()

        response_time = (end_time - start_time) * 1000
        response_time = int(response_time)

        logging_event_hook.fire(
            method = "Selenium",
            name = "Enter Asset Account name",
            content_length = 0, # Ở HttpUser là kích thước của các response (đơn vị byte)
            response_time = response_time
        )

    @task
    def store_new_asset_account(self):
        '''
            Bấm nút lưu Asset Account
        '''
        start_time = time.time()

        selenium_utils.store_new_asset_account(self.browser)

        end_time = time.time()

        response_time = (end_time - start_time) * 1000
        response_time = int(response_time)

        logging_event_hook.fire(
            method = "Selenium",
            name = "Store new Asset Account",
            content_length = 0, # Ở HttpUser là kích thước của các response (đơn vị byte)
            response_time = response_time
        )

    @task
    def check_if_asset_account_was_successfully_created(self):
        '''
            Kiểm tra xem Asset Account đã được tạo thành công hay chưa
        '''
        start_time = time.time()

        is_test_case_passed = selenium_utils.was_asset_account_successfully_created(
            self.browser, 
            selenium_utils.create_asset_account_name(self.init_time)
        )

        end_time = time.time()

        # Nếu test case đã được tạo thành công thì append vào file success test cases
        if is_test_case_passed:
            with open(f"{self.report_dir}/success_test_cases.json", 'r') as file:
                success_test_cases = json.load(file)
                success_test_cases.append({
                    "Time": self.init_time,
                    "Name": selenium_utils.create_asset_account_name(self.init_time)
                })
        else:
            with open(f"{self.report_dir}/failed_test_cases.json", 'r') as file:
                failed_test_cases = json.load(file)
                failed_test_cases.append({
                    "Time": self.init_time,
                    "Name": selenium_utils.create_asset_account_name(self.init_time)
                })

        response_time = (end_time - start_time) * 1000
        response_time = int(response_time)

        logging_event_hook.fire(
            method = "Selenium",
            name = "Go to Asset Account list page",
            content_length = 0, # Ở HttpUser là kích thước của các response (đơn vị byte)
            response_time = response_time
        )

    @task
    def clean_after_running(self):
        try:
            os.system(f"lsof -ti tcp:{self.free_port} | xargs kill -9")
            if os.path.exists(self.browser_instance_data_dir):
                shutil.rmtree(self.browser_instance_data_dir)
        except:
            pass

    def on_stop(self):
        try:
            os.system(f"lsof -ti tcp:{self.free_port} | xargs kill -9")
            if os.path.exists(self.browser_instance_data_dir):
                shutil.rmtree(self.browser_instance_data_dir)
        except:
            pass

class MyUser(User):
    tasks = [SequentialSeleniumTasks]

    def logging_event_handler(self, method, name, content_length, response_time):

        print(f"Event was fired with arguments: {method}, {name}")

        self.environment.runner.stats.log_request(
            method=method,
            content_length=content_length,
            name=name, 
            response_time=response_time
        )

    def on_start(self):
        logging_event_hook.add_listener(self.logging_event_handler)
