import tkinter
import tkinter.messagebox
import customtkinter
from tkinter import filedialog
import os
import time

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_widget_scaling(1.0)  # Set UI scaling to 100% by default

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.deleted_files = []

        # configure window
        self.title("Upload and Download File")
        self.geometry(f"{1100}x{620}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
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
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Enter URL of File")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, text="Search", border_width=2)
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.textbox.insert("0.0", "Process Activity Log :\n\n" + "Log-Message \"Application started\"\n" + "Log-Message \"User logged in\"\n" + "Log-Message \"Data updated\"\n\n" + "This screen will show the activities you perform in this application. That processes will be shown below...\n\n")

        # create clock and calendar by tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
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
        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.radiobutton_frame.grid_columnconfigure(0, weight=1)  # Adjusted to center-align content

        self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="Notification", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.label_radio_group.grid(row=0, column=0, pady=(10, 0), padx=20, sticky="n")
        
        self.radio_1 = customtkinter.CTkLabel(master=self.radiobutton_frame, text="Application started : Successful")
        self.radio_1.grid(row=1, column=0, pady=5, padx=20, sticky="n")
        
        self.radio_2 = customtkinter.CTkLabel(master=self.radiobutton_frame, text="User logged in : Successful")
        self.radio_2.grid(row=2, column=0, pady=5, padx=20, sticky="n")
        
        self.radio_3 = customtkinter.CTkLabel(master=self.radiobutton_frame, text="Data updated : Successful")
        self.radio_3.grid(row=3, column=0, pady=5, padx=20, sticky="n")
        
        self.radio_4 = customtkinter.CTkLabel(master=self.radiobutton_frame, text="All processes successfully.")
        self.radio_4.grid(row=4, column=0, pady=5, padx=20, sticky="n")
        
        self.name_notification = customtkinter.CTkLabel(master=self.radiobutton_frame, text="Welcome to Our Application.\nHope you have a good experience!")
        self.name_notification.grid(row=5, column=0, pady=5, padx=20, sticky="n")

        self.radio_var = tkinter.IntVar(value=0)

        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
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
        self.help_frame = customtkinter.CTkScrollableFrame(self, label_text="Help - FAQ")
        self.help_frame.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.help_frame.grid_columnconfigure(0, weight=1)

        self.faq_questions = [
            "How to upload a file?",
            "How to download a file?",
            "How to delete a file?",
            "How to restore a file from bin?",
            "How to change language?",
            "How to change appearance mode?",
            "How to change scaling?",
            "How to search by file URL?",
            "How to starred a file?"
        ]

        self.faq_answers = {
            "How to upload a file?": "To upload a file, click on the 'Upload' button in the sidebar and select the file you want to upload.",
            "How to download a file?": "To download a file, click on the 'Download' button in the sidebar and select the file you want to download.",
            "How to delete a file?": "To delete a file, select the file and click on the 'Delete' button. The file will be moved to the recycle bin.",
            "How to restore a file from recycle bin?": "To restore a file from the recycle bin, click on the 'Recycle Bin' button in the sidebar, select the file, and click 'Restore'.",
            "How to change language?": "To change the language, click on the 'Language' button in the sidebar. This will toggle between English and Vietnamese.",
            "How to change appearance mode?": "To change the appearance mode, select the desired mode from the 'Appearance Mode' dropdown in the sidebar.",
            "How to change scaling?": "To change the UI scaling, select the desired scaling from the 'UI Scaling' dropdown in the sidebar.",
            "How to search by file URL?": "To search by file URL, enter the URL in the search box and click the 'Search' button.",
            "How to starred a file?": "To starred a file, click on the 'Starred File' button in the sidebar. This will mark the file as starred."
        }

        for question in self.faq_questions:
            button = customtkinter.CTkButton(self.help_frame, text=question, command=lambda q=question: self.show_answer(q))
            button.pack(pady=5, padx=10)

        # create contact us frame
        self.contact_us_frame = customtkinter.CTkFrame(self)
        self.contact_us_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.contact_label = customtkinter.CTkLabel(master=self.contact_us_frame, text="Contact Us", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.contact_label.grid(row=0, column=0, pady=10, padx=20, sticky="n")

        self.name_label = customtkinter.CTkLabel(master=self.contact_us_frame, text="Team : Your Team")
        self.name_label.grid(row=1, column=0, pady=5, padx=20, sticky="n")

        self.email_label = customtkinter.CTkLabel(master=self.contact_us_frame, text="Email : example@gmail.com")
        self.email_label.grid(row=2, column=0, pady=5, padx=20, sticky="n")

        self.phone_label = customtkinter.CTkLabel(master=self.contact_us_frame, text="Phone : +123456789")
        self.phone_label.grid(row=3, column=0, pady=5, padx=20, sticky="n")

        self.address_label = customtkinter.CTkLabel(master=self.contact_us_frame, text="Address : 227 Nguyen Van Cu\nWard 4, District 5, Ho Chi Minh City")
        self.address_label.grid(row=4, column=0, pady=5, padx=20, sticky="n")

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
