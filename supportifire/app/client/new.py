import threading
import requests
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES

def download_file(url, file_name):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        messagebox.showinfo("Success", f"Download completed: {file_name}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def upload_file(url, file_path):
    try:
        with open(file_path, 'rb') as file:
            response = requests.post(url, files={'file': file})
            response.raise_for_status()
        messagebox.showinfo("Success", f"Upload completed: {file_path}, Status Code: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def start_download():
    url = url_entry.get()
    file_name = file_name_entry.get()
    if url and file_name:
        threading.Thread(target=download_file, args=(url, file_name)).start()
    else:
        messagebox.showwarning("Input Error", "Please provide both URL and file name.")

def start_upload():
    file_path = filedialog.askopenfilename()
    if file_path:
        threading.Thread(target=upload_file, args=(upload_url_entry.get(), file_path)).start()
    else:
        messagebox.showwarning("Input Error", "Please select a file to upload.")

def drop(event):
    file_path = event.data
    if file_path:
        threading.Thread(target=upload_file, args=(upload_url_entry.get(), file_path)).start()


# UI START HERE
# Create main window
root = TkinterDnD.Tk()
root.title("File Downloader/Uploader")

# Download section
tk.Label(root, text="Download URL:").grid(row=0, column=0, padx=10, pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Save as:").grid(row=1, column=0, padx=10, pady=10)
file_name_entry = tk.Entry(root, width=50)
file_name_entry.grid(row=1, column=1, padx=10, pady=10)

download_button = tk.Button(root, text="Download", command=start_download)
download_button.grid(row=2, column=0, columnspan=2, pady=10)

# Upload section
tk.Label(root, text="Upload URL:").grid(row=3, column=0, padx=10, pady=10)
upload_url_entry = tk.Entry(root, width=50)
upload_url_entry.grid(row=3, column=1, padx=10, pady=10)

upload_button = tk.Button(root, text="Upload", command=start_upload)
upload_button.grid(row=4, column=0, columnspan=2, pady=10)

# Drag and Drop area
drop_area = tk.Label(root, text="Drag and Drop Files Here", bg="white", relief="groove", width=50, height=10)
drop_area.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

drop_area.drop_target_register(DND_FILES)
drop_area.dnd_bind('<<Drop>>', drop)

# Run the application
root.mainloop()
