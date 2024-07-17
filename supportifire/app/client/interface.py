import tkinter
import customtkinter
from tkinter import filedialog, messagebox
import os
import time

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_widget_scaling(1.0)  # Set UI scaling to 100% by default

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        # initialize user data
        self.users = {"admin": "admin"}  
        self.current_user = None

        # deleted files list
        self.deleted_files = []

        # configure window
        self.title("Upload and Download File")
        self.geometry(f"{1100}x{620}")
        
        # create login frame
        self.login_frame = customtkinter.CTkFrame(self, width=400, height=300, corner_radius=0)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.login_label = customtkinter.CTkLabel(self.login_frame, text="Login", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.login_label.grid(row=0, column=0, padx=20, pady=(20, 10), columnspan=2)

        self.username_entry = customtkinter.CTkEntry(self.login_frame, placeholder_text="Username")
        self.username_entry.grid(row=1, column=0, padx=20, pady=10, columnspan=2)

        self.password_entry = customtkinter.CTkEntry(self.login_frame, placeholder_text="Password", show="*")
        self.password_entry.grid(row=2, column=0, padx=20, pady=10, columnspan=2)

        self.login_button = customtkinter.CTkButton(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=3, column=0, padx=20, pady=10)

        self.register_button = customtkinter.CTkButton(self.login_frame, text="Register", command=self.show_register_frame)
        self.register_button.grid(row=3, column=1, padx=20, pady=10)

        # create register frame
        self.register_frame = customtkinter.CTkFrame(self, width=400, height=300, corner_radius=0)

        self.register_label = customtkinter.CTkLabel(self.register_frame, text="Register", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.register_label.grid(row=0, column=0, padx=20, pady=(20, 10), columnspan=2)

        self.new_username_entry = customtkinter.CTkEntry(self.register_frame, placeholder_text="Username")
        self.new_username_entry.grid(row=1, column=0, padx=20, pady=10, columnspan=2)

        self.new_password_entry = customtkinter.CTkEntry(self.register_frame, placeholder_text="Password", show="*")
        self.new_password_entry.grid(row=2, column=0, padx=20, pady=10, columnspan=2)

        self.confirm_password_entry = customtkinter.CTkEntry(self.register_frame, placeholder_text="Confirm Password", show="*")
        self.confirm_password_entry.grid(row=3, column=0, padx=20, pady=10, columnspan=2)

        self.create_account_button = customtkinter.CTkButton(self.register_frame, text="Create Account", command=self.register)
        self.create_account_button.grid(row=4, column=0, padx=20, pady=10)

        self.back_to_login_button = customtkinter.CTkButton(self.register_frame, text="Back to Login", command=self.show_login_frame)
        self.back_to_login_button.grid(row=4, column=1, padx=20, pady=10)

        # create main frame for file manager
        self.main_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        
        # configure grid layout (4x4)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure((2, 3), weight=0)
        self.main_frame.grid_rowconfigure((0, 1, 2), weight=1)
        
        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self.main_frame, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="File Manager", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Upload", command=self.upload_file)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Download", command=self.download_file)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Recycle Bin", command=self.open_trash_bin)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        self.language_button = customtkinter.CTkButton(self.sidebar_frame, text="English", command=self.change_language_event)
        self.language_button.grid(row=4, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.set("100%")
        self.scaling_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self.main_frame, placeholder_text="Enter URL of File")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self.main_frame, text="Search", border_width=2)
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self.main_frame, width=250)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.textbox.insert("0.0", "Process Activity Log :\n\n" + "Log-Message \"Application started\"\n" + "Log-Message \"User logged in\"\n" + "Log-Message \"Data updated\"\n\n" + "This screen will show the activities you perform in this application. That processes will be shown below...\n\n")

        # create clock and calendar by tabview
        self.tabview = customtkinter.CTkTabview(self.main_frame, width=0)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Time by hours")
        self.tabview.add("Time by dates")
        self.tabview.tab("Time by hours").grid_columnconfigure(0, weight=1)  
        self.tabview.tab("Time by dates").grid_columnconfigure(0, weight=1)

        self.label_tab_1 = customtkinter.CTkButton(self.tabview.tab("Time by hours"), text="Hours : Minutes")
        self.label_tab_1.grid(row=2, column=0, padx=20, pady=(20, 20))
        self.label_tab_2 = customtkinter.CTkButton(self.tabview.tab("Time by dates"), text="Dates - Months")
        self.label_tab_2.grid(row=2, column=0, padx=20, pady=(20, 20))
        
        # create real-time digital clock
        self.clock_label = customtkinter.CTkLabel(self.tabview.tab("Time by hours"), text="", font=("Arial", 60))
        self.clock_label.grid(row=3, column=0, padx=20, pady=20)
        self.update_clock()
        
        # create real-time digital calendar
        self.date_label = customtkinter.CTkLabel(self.tabview.tab("Time by dates"), text="", font=("Arial", 60))
        self.date_label.grid(row=3, column=0, padx=20, pady=20)
        self.update_date_month()

        # create notification frame
        self.radiobutton_frame = customtkinter.CTkFrame(self.main_frame)
        self.radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.radiobutton_frame.grid_columnconfigure(0, weight=1)  

        self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="Notification", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label_radio_group.grid(row=0, column=0, pady=(10, 0), padx=20, sticky="n")
        
        self.radio_1 = customtkinter.CTkLabel(master=self.radiobutton_frame, text="Application started")
        self.radio_1.grid(row=1, column=0, pady=5, padx=20, sticky="n")
        
        self.radio_2 = customtkinter.CTkLabel(master=self.radiobutton_frame, text="User logged in")
        self.radio_2.grid(row=2, column=0, pady=5, padx=20, sticky="n")
        
        self.radio_3 = customtkinter.CTkLabel(master=self.radiobutton_frame, text="Data updated")
        self.radio_3.grid(row=3, column=0, pady=5, padx=20, sticky="n")
        
        self.radio_4 = customtkinter.CTkLabel(master=self.radiobutton_frame, text="All processes successfully")
        self.radio_4.grid(row=4, column=0, pady=5, padx=20, sticky="n")

        self.radio_var = tkinter.IntVar(value=0)

        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self.main_frame, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        
        self.upload_file_button = customtkinter.CTkButton(self.slider_progressbar_frame, text="All Server File", command=self.upload_folder)
        self.upload_file_button.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.upload_folder_button = customtkinter.CTkButton(self.slider_progressbar_frame, text="Starred File", command=self.upload_folder)
        self.upload_folder_button.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")        
        
        self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_1.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.progressbar_2 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_2.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        
        self.slider_1 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=1, number_of_steps=3)
        self.slider_1.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_2 = customtkinter.CTkSlider(self.slider_progressbar_frame, orientation="vertical")
        self.slider_2.grid(row=0, column=1, rowspan=5, padx=(10, 10), pady=(10, 10), sticky="ns")
        self.progressbar_3 = customtkinter.CTkProgressBar(self.slider_progressbar_frame, orientation="vertical")
        self.progressbar_3.grid(row=0, column=2, rowspan=5, padx=(10, 20), pady=(10, 10), sticky="ns")

        # create help frame with FAQ
        self.help_frame = customtkinter.CTkScrollableFrame(self.main_frame, label_text="Help - FAQ")
        self.help_frame.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.help_frame.grid_columnconfigure(0, weight=1)

        self.faq_questions = [
            "How to upload a file?",
            "How to download a file?",
            "How to delete a file?",
            "How to search by file URL?",
            "How to change scaling?",
            "How to change language?",
            "How to restore a file?",
            "How to change appearance mode?",
            "How to starred a file?"
        ]

        self.faq_answers = {
            "How to upload a file?": "To upload a file, click on the 'Upload' button in the sidebar and select the file you want to upload.",
            "How to download a file?": "To download a file, click on the 'Download' button in the sidebar and select the file you want to download.",
            "How to delete a file?": "To delete a file, select the file and click on the 'Delete' button. The file will be moved to the recycle bin.",
            "How to search by file URL?": "To search by file URL, enter the URL in the search box and click the 'Search' button.",
            "How to change scaling?": "To change the UI scaling, select the desired scaling from the 'UI Scaling' dropdown in the sidebar.",
            "How to change language?": "To change the language, click on the 'Language' button in the sidebar. This will toggle between English and Vietnamese.",            
            "How to restore a file?": "To restore a file from the recycle bin, click on the 'Recycle Bin' button in the sidebar, select the file, and click 'Restore'.",
            "How to change appearance mode?": "To change the appearance mode, select the desired mode from the 'Appearance Mode' dropdown in the sidebar.",
            "How to starred a file?": "To starred a file, click on the 'Starred File' button in the sidebar. This will mark the file as starred."
        }

        for question in self.faq_questions:
            button = customtkinter.CTkButton(self.help_frame, text=question, command=lambda q=question: self.show_answer(q))
            button.pack(pady=5, padx=10)

        # create contact us frame
        self.contact_us_frame = customtkinter.CTkFrame(self.main_frame)
        self.contact_us_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.contact_label = customtkinter.CTkLabel(master=self.contact_us_frame, text="Contact Us", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.contact_label.grid(row=0, column=0, pady=10, padx=20, sticky="n")

        self.name_label = customtkinter.CTkLabel(master=self.contact_us_frame, text="Team : Your Team")
        self.name_label.grid(row=1, column=0, pady=5, padx=20, sticky="n")

        self.email_label = customtkinter.CTkLabel(master=self.contact_us_frame, text="Email : example@gmail.com")
        self.email_label.grid(row=2, column=0, pady=5, padx=20, sticky="n")

        self.phone_label = customtkinter.CTkLabel(master=self.contact_us_frame, text="Phone : +123456789")
        self.phone_label.grid(row=3, column=0, pady=5, padx=20, sticky="n")

        self.address_label = customtkinter.CTkLabel(master=self.contact_us_frame, text="Address : 227 Nguyen Van Cu\nWard 4, District 5\nHo Chi Minh City, Viet Nam")
        self.address_label.grid(row=4, column=0, pady=5, padx=20, sticky="n")
        
    # create a function to show login frame
    def show_login_frame(self):
        self.register_frame.place_forget()
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

    # create a function to show register frame
    def show_register_frame(self):
        self.login_frame.place_forget()
        self.register_frame.place(relx=0.5, rely=0.5, anchor="center")

    # create a function to open folder manager
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.users and self.users[username] == password:
            self.current_user = username
            self.login_frame.place_forget()
            self.main_frame.grid(row=0, column=0, sticky="nsew")
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)
            self.textbox.insert("end", f"Welcome, {username}!\n")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    # create a function to register
    def register(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if username in self.users:
            messagebox.showerror("Registration Failed", "Username already exists")
        elif password != confirm_password:
            messagebox.showerror("Registration Failed", "Passwords do not match")
        else:
            self.users[username] = password
            messagebox.showinfo("Registration Successful", "Account created successfully")
            self.show_login_frame()

    # create a function to log activities
    def log_activity(self, message):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.textbox.insert(tkinter.END, f"{timestamp} - {message}\n")
        self.textbox.yview(tkinter.END)  

    # change appearance mode event
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
        self.log_activity(f"Changed appearance mode to {new_appearance_mode}.")

    # change scaling event
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
        self.log_activity(f"Changed scaling to {new_scaling}.")

    # update clock vietnam
    def update_clock(self):
        vietnam_hours = time.strftime('%H:%M')
        self.clock_label.configure(text=vietnam_hours)
        self.after(1000, self.update_clock)

    # update date month
    def update_date_month(self):
        vietnam_dates = time.strftime('%d-%m')
        self.date_label.configure(text=vietnam_dates)
        self.after(86400000, self.update_date_month)
        
    # create a function to show answer
    def show_answer(self, question):
        answer = self.faq_answers.get(question, "Answer not found.")
        tkinter.messagebox.showinfo("Answer", answer)
        self.log_activity(f"FAQ: {question}")

    # change language event
    def change_language_event(self):
        current_text = self.language_button.cget("text")
        if current_text == "English":
            self.logo_label.configure(text="Quản lý Tệp")
            self.language_button.configure(text="Tiếng Việt")
            self.sidebar_button_1.configure(text="Tải lên")
            self.sidebar_button_2.configure(text="Tải xuống")
            self.sidebar_button_3.configure(text="Thùng rác")
            self.appearance_mode_label.configure(text="Chế độ giao diện:")
            self.scaling_label.configure(text="Tỷ lệ giao diện:")
            self.label_tab_1.configure(text="Giờ : Phút")
            self.label_tab_2.configure(text="Ngày - Tháng")
            self.help_frame.configure(label_text="Trợ giúp - Câu hỏi thường gặp")
            self.upload_file_button.configure(text="Tất cả tệp trên máy chủ")
            self.upload_folder_button.configure(text="Tệp được đánh dấu")
            self.label_radio_group.configure(text="Thông báo")
            self.contact_label.configure(text="Liên hệ với chúng tôi")
            self.entry.configure(placeholder_text="Nhập URL của tệp")
            self.main_button_1.configure(text="Tìm kiếm")
            self.log_activity("Đã chuyển sang tiếng Việt.")
        else:
            self.logo_label.configure(text="File Manager")
            self.language_button.configure(text="English")
            self.sidebar_button_1.configure(text="Upload")
            self.sidebar_button_2.configure(text="Download")
            self.sidebar_button_3.configure(text="Recycle Bin")
            self.appearance_mode_label.configure(text="Appearance Mode:")
            self.scaling_label.configure(text="UI Scaling:")
            self.label_tab_1.configure(text="Hours : Minutes")
            self.label_tab_2.configure(text="Dates - Months")
            self.help_frame.configure(label_text="Help - FAQ")
            self.upload_file_button.configure(text="All Server File")
            self.upload_folder_button.configure(text="Starred File")
            self.label_radio_group.configure(text="Notification")
            self.contact_label.configure(text="Contact Us")
            self.entry.configure(placeholder_text="Enter URL of File")
            self.main_button_1.configure(text="Search")
            self.log_activity("Switched to English.")

    # upload file functions
    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.log_activity(f"Uploaded file: {file_path}")

    # download file functions
    def download_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            download_location = filedialog.askdirectory()
            if download_location:
                destination = os.path.join(download_location, os.path.basename(file_path))
                with open(file_path, 'rb') as src_file:
                    with open(destination, 'wb') as dest_file:
                        dest_file.write(src_file.read())
                self.log_activity(f"Downloaded file: {file_path} to {download_location}")

    # open trash bin function
    def open_trash_bin(self):
        trash_bin_window = customtkinter.CTkToplevel(self)
        trash_bin_window.title("Recycle Bin")
        trash_bin_window.geometry("400x300")
        trash_bin_window.attributes('-topmost', True)

        for index, file_path in enumerate(self.deleted_files):
            label = customtkinter.CTkLabel(trash_bin_window, text=file_path)
            label.pack()

        restore_button = customtkinter.CTkButton(trash_bin_window, text="Restore Selected", command=lambda: self.restore_file(trash_bin_window))
        restore_button.pack(pady=10)
        self.log_activity("Opened Recycle Bin.")

    # restore file function
    def restore_file(self, window):
        selected_file = None
        for widget in window.winfo_children():
            if isinstance(widget, customtkinter.CTkLabel) and widget.cget("text") in self.deleted_files:
                selected_file = widget.cget("text")
                break

        if selected_file:
            self.deleted_files.remove(selected_file)
            self.log_activity(f"Restored file: {selected_file}")

    # open folder manager function
    def upload_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.log_activity(f"Uploaded folder: {folder_path}")
            self.open_folder_manager(folder_path)
        self.log_activity("Opened folder manager.")
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
