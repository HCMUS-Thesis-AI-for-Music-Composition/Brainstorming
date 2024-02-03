import datetime
import socket
import shutil
import os

# IP của server được deploy trên Google Cloud 
# (tài khoản deploy có thể hết ngân sách sau deadline nên có thể làm web không chạy được)
server_ip = "34.16.184.203"

# URL đến trang đăng nhập
login_url = f"http://{server_ip}/login"

# URL đến trang danh sách tài khoản dạng asset
asset_account_list_url = f"http://{server_ip}/accounts/asset"

# URL đến trang tạo tài khoản dạng asset
create_asset_account_url = f"http://{server_ip}/accounts/create/asset"

email = "20120406@student.hcmus.edu.vn"

browser_instance_data_dir = "/Users/4rr311/Documents/VectorA/KHTN/Nam4/HKI/Kiem thu phan mem/Project/Final-Project/Performance Testing/Source/browser_instance_data"

report_folder = "/Users/4rr311/Documents/VectorA/KHTN/Nam4/HKI/Kiem thu phan mem/Project/Final-Project/Performance Testing/Source/test_report"

def current_datetime(datetime_format: str = "%H:%M:%S %d/%m/%Y") -> str:
    '''
        Lấy ngày giờ hệ thống
    '''
    
    # Lấy ngày giờ hiện tại
    curr_datetime = datetime.datetime.now()

    # Format ngày giờ theo định dạng chỉ định
    curr_datetime = curr_datetime.strftime(datetime_format)

    return curr_datetime


def read_file(file_path) -> str:
    '''
        Hàm đọc file văn bản
    '''

    try:
        with open(file_path, 'r') as file:
            file_contents = file.read()

        return file_contents
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"An error occurred: {str(e)}"
    

def read_password(file_name: str = "password.pass") -> str:
    '''
        Hàm đọc password của tài khoản email (để không trình chiếu password khi thuyết trình)
    '''

    # Tạo file lưu password nếu chưa tồn tại
    os.system(f'touch "{file_name}"')

    password = read_file(f'./{file_name}')

    return password

password = read_file("password.pass")

def find_free_port(min_port: int = 40000, max_port: int = 42000):
    '''
        Tìm một port trống trên máy
    '''

    for port in range(min_port, max_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(("127.0.0.1", port))
            # sock.close()
            return [port, sock]  # Trả về port trống nếu tìm thấy
        except OSError:
            continue  # Nếu port đã được sử dụng, tiếp tục tìm port khác
    return None  # Trả về None nếu không tìm thấy port trống trong phạm vi chỉ định


# LEGACY CODE (from our seminar)

# def copy_folder_content(source_folder, dest_folder):
#     '''
#         Copy toàn bộ nội dung từ source_folder vào dest_folder (tạo mới nếu dest_folder chưa tồn tại)
#     '''
#     # Xoá thư mục dest_folder nếu đã tồn tại
#     if os.path.exists(dest_folder):
#         shutil.rmtree(dest_folder)

#     os.makedirs(dest_folder)
    
#     # Sao chép nội dung từ thư mục nguồn vào thư mục đích
#     for item in os.listdir(source_folder):
#         source_item = os.path.join(source_folder, item)
#         destination_item = os.path.join(dest_folder, item)
#         if os.path.isdir(source_item):
#             shutil.copytree(source_item, destination_item, symlinks=True)
#         else:
#             shutil.copy2(source_item, destination_item)