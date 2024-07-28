import socket
import os
import threading
import csv
import shutil

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Change all file and user login csv files to string
def csv_to_string(file_path):
    result = ""
    with open(file_path, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            account, password = row
            result += f"{account}:{password}|"
    return result

# Change recycle bin and starred files csv files to string
def extract_user_info(file_path, user_name):
    result = ""
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)

        for row in csv_reader:
            if row[0] == user_name:
                for i in range(1, len(row), 2):
                    if i+1 < len(row):
                        result += f"{row[i]}:{row[i+1]}|"
                break
    return result

# Add new row to csv file by id and info (all file and user login)
def add_new_row(file_path, new_id, new_info):
    rows = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)
        rows.append(headers)

        for row in csv_reader:
            rows.append(row)
    
    # Tạo dòng mới
    new_row = [new_id, new_info]
    rows.append(new_row)
    
    # Ghi lại file CSV với dòng mới
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(rows)

# Add new row to csv file by username (recycle bin and starred files)
def add_new_user(file_path, new_user):
    rows = []
    
    # Đọc file CSV và lưu lại các dòng
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            rows.append(row)
    
    # Tạo dòng mới chỉ với tên người dùng
    new_row = [new_user]
    rows.append(new_row)
    
    # Ghi lại file CSV với dòng mới
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(rows)

# Restore file from recycle bin (xóa 1 id trên 1 dòng đã cho trước và có thể dùng cho unstarred file)
def del_one_id_in_one_row(file_path, user_name, id_to_del):
    rows = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)
        rows.append(headers)

        for row in csv_reader:
            if row[0] == user_name:
                # Tìm và xóa cặp định dạng yêu cầu
                for i in range(1, len(row), 2):
                    if row[i] == id_to_del:
                        row[i] = ''
                        row[i+1] = ''
                # Loại bỏ các cột rỗng
                row = [item for item in row if item]
            rows.append(row)
    
    # Ghi lại file CSV với các thay đổi
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(rows)

# When user remove file to recycle bin, remove file from starred file of all users
def remove_id_from_starred(file_path, id_to_remove):
    rows = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)
        rows.append(headers)

        for row in csv_reader:
            # Tìm và xóa cặp định dạng yêu cầu cho tất cả các dòng
            for i in range(1, len(row), 2):
                if row[i] == id_to_remove:
                    row[i] = ''
                    row[i+1] = ''
            # Loại bỏ các cột rỗng
            row = [item for item in row if item]
            rows.append(row)
    
    # Ghi lại file CSV với các thay đổi
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(rows)
        
# Tìm id và xóa dòng chứa id đó (all file)        
def remove_row_by_id(file_path, id_to_remove):
    rows = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)
        rows.append(headers)

        for row in csv_reader:
            # Chỉ thêm các dòng không chứa ID cần xóa
            if row[0] != id_to_remove:
                rows.append(row)
    
    # Ghi lại file CSV với các thay đổi
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(rows)
        
# Add new info to 1 row in csv file (starred file and recycle bin)
def add_info_to_user(file_path, target_user, new_id, new_account_info):
    rows = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)
        rows.append(headers)

        for row in csv_reader:
            if row[0] == target_user:
                row.extend([new_id, new_account_info])
            rows.append(row)
    
    # Ghi lại file CSV với các thay đổi
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(rows)
        
# Move file from source to destination
def move_file(source_file, destination_folder):
    os.makedirs(destination_folder, exist_ok=True)
    shutil.move(source_file, destination_folder)
    print(f"File '{source_file}' đã được chuyển đến '{destination_folder}'")

# Handle client function
def handle_client(client_socket):
    try:
        received = client_socket.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)
        filename = os.path.basename(filename)
        filesize = int(filesize)
        
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        with open(filepath, "wb") as f:
            while True:
                bytes_read = client_socket.recv(BUFFER_SIZE)
                if not bytes_read:    
                    break
                f.write(bytes_read)
        print(f"File {filename} received successfully")
    finally:
        client_socket.close()

def start_server():
    # All file paths
    file_path_all_files = '/Users/admin/Desktop/Node/python_project/server/data_users/all_file.csv'
    file_path_recycle_bin = '/Users/admin/Desktop/Node/python_project/server/data_users/recycle_bin.csv'
    file_path_starred_files = '/Users/admin/Desktop/Node/python_project/server/data_users/starred_file.csv'
    file_path_users_login = '/Users/admin/Desktop/Node/python_project/server/data_users/users_login.csv'
    
    # Convert csv users login files to string
    csv_users_login = csv_to_string(file_path_users_login)
    
    # Send users login string to client
    
    # Get user login info from client
    user_now = "user1"
    
    # Get all files string
    csv_all_files = csv_to_string(file_path_all_files)
    
    # Get recycle bin string and starred files string
    csv_recycle_bin = extract_user_info(file_path_recycle_bin, user_now)
    csv_starred_files = extract_user_info(file_path_starred_files, user_now)
    
    # Send all files string, recycle bin string and starred files string to client
    
    
    # Start server
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
    
    while True:
        client_socket, address = server_socket.accept()
        print(f"[+] {address} is connected.")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
