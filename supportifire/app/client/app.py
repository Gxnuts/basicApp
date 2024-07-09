import tkinter as tk
from tkinter import filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
import socket
import os

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5001
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

def upload_to_server(file_path):
    filesize = os.path.getsize(file_path)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    
    client_socket.send(f"{file_path}{SEPARATOR}{filesize}".encode())
    
    with open(file_path, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            client_socket.sendall(bytes_read)
    client_socket.close()
    print(f"File {file_path} uploaded successfully")

def drop(event):
    file_path = event.data
    upload_to_server(file_path)

def upload_file():
    filename = filedialog.askopenfilename()
    upload_to_server(filename)

def create_new_folder():
    print("New Folder button clicked")





# Initialize the main window
root = TkinterDnD.Tk()
root.title("File Upload App")
root.geometry("1024x768")

# Sidebar
sidebar = tk.Frame(root, width=200, bg='#f1f1f1', height=768, relief='sunken', borderwidth=2)
sidebar.pack(expand=False, fill='y', side='left', anchor='nw')

# Sidebar content
sidebar_label = tk.Label(sidebar, text="Sidebar", bg='#f1f1f1')
sidebar_label.pack()

for i in ["Pictures", "Videos", "Documents", "Music", "Others"]:
    btn = tk.Button(sidebar, text=i, relief='flat')
    btn.pack(fill='x')

# Main content area
main_content = tk.Frame(root, bg='#ffffff', width=800, height=768)
main_content.pack(expand=True, fill='both', side='right')

# Toolbar
toolbar = tk.Frame(main_content, bg='#e0e0e0', height=50, relief='raised', borderwidth=2)
toolbar.pack(expand=False, fill='x')

upload_button = tk.Button(toolbar, text="Upload", command=upload_file)
upload_button.pack(side=tk.LEFT, padx=10, pady=10)

new_folder_button = tk.Button(toolbar, text="New folder", command=create_new_folder)
new_folder_button.pack(side=tk.LEFT, padx=10, pady=10)

# File display area
file_display = tk.Frame(main_content, bg='#ffffff', padx=10, pady=10)
file_display.pack(expand=True, fill='both')

# Example files (for illustration)
for i in range(3):
    file_frame = tk.Frame(file_display, bg='#f9f9f9', relief='groove', borderwidth=1, width=100, height=100)
    file_frame.grid(row=0, column=i, padx=10, pady=10)
    file_label = tk.Label(file_frame, text=f"File {i+1}", bg='#f9f9f9')
    file_label.pack(expand=True)

# Drop area
drop_area = tk.Label(file_display, text="Upload files", bg='#ffffff', fg='black', relief='solid', borderwidth=2, width=20, height=10)
drop_area.grid(row=0, column=3, padx=10, pady=10)

drop_area.drop_target_register(DND_FILES)
drop_area.dnd_bind('<<Drop>>', drop)

root.mainloop()
