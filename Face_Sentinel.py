import sys
import time
import threading
import customtkinter
import subprocess
import clr  # Python.net
from pystray import MenuItem as item
import pystray
from PIL import Image
import configparser
from distutils.util import strtobool
import datetime
from pathlib import Path
from tendo import singleton
import winsdk.windows.security.credentials.ui as wscu
import asyncio
import winsound

clr.AddReference("System.Diagnostics.Process")
from System.Diagnostics import Process
import Main_Authorization


me = singleton.SingleInstance()  # Prevents multiple startups


# ------ Configure -------
config = configparser.ConfigParser()
config.read("./config.ini")

debugging = strtobool(config["settings"]["debugging"])
limit = int((config["settings"]["limit"]))  # It may be changed by GUI input
your_pics_dir = config["settings"]["your_pics_dir"]
capture_pics_dir = config["settings"]["capture_pics_dir"]
tolerate_target_face__errors = strtobool(
    config["settings"]["tolerate_target_face__errors"]
)
rigidity = int((config["settings"]["rigidity"]))
threshold = float((config["settings"]["threshold"]))
# ------------------------

known_image_preparation = Main_Authorization.known_pics_prepare(your_pics_dir, debugging)
if(known_image_preparation == -2 and tolerate_target_face__errors == False):
    sys.exit()

# --- Global Variables ---
tolerate_target_face__errors_text = ["撮影時エラーを許容しない", "撮影時エラーを許容する"]
# ------------------------


class App(customtkinter.CTk):  # CustomTKinter (GUI) Class
    def __init__(self):
        super().__init__()
        self.fonts = ("meiryo", 15)
        self.iconbitmap("Assets/headandlock.ico")
        self.geometry(
            "400x215+" + str(self.winfo_screenwidth() / 2) + "+" + str(10)
        )  # Setting form size
        # self.attributes("-topmost", 1)   # Display at the front
        self.title("Face Sentinel")
        self.setup_form()  # setup form

    def setup_form(self):
        global limit
        global tolerate_target_face__errors

        # main logo
        logo_image = customtkinter.CTkImage(
            Image.open("Assets/FS_logo.png"), size=(250, 50)
        )
        self.logo_label = customtkinter.CTkLabel(
            master=self, text="", image=logo_image, font=self.fonts
        )
        self.logo_label.place(x=67, y=4)

        # interval widgets
        self.textbox = customtkinter.CTkEntry(
            master=self,
            placeholder_text="動作間隔: " + str(limit) + "s",
            width=120,
            font=self.fonts,
        )
        self.textbox.place(x=5, y=60)
        self.button = customtkinter.CTkButton(
            master=self,
            text="適用",
            width=50,
            command=self.apply_button_function,
            font=self.fonts,
        )
        self.button.place(x=130, y=60)

        # threshold widgets
        self.threshold_textbox = customtkinter.CTkEntry(
            master=self,
            placeholder_text="類似度閾値:" + str(threshold),
            width=120,
            font=self.fonts,
        )
        self.threshold_textbox.place(x=5, y=95)
        self.threshold_apply_button = customtkinter.CTkButton(
            master=self,
            text="適用",
            width=50,
            command=self.threshold_apply_button_function,
            font=self.fonts,
        )
        self.threshold_apply_button.place(x=130, y=95)

        # rigidity widgets
        self.rigidity_textbox = customtkinter.CTkEntry(
            master=self,
            placeholder_text="判定閾値:" + str(rigidity) + "%",
            width=120,
            font=self.fonts,
        )
        self.rigidity_textbox.place(x=5, y=130)
        self.rigidity_apply_button = customtkinter.CTkButton(
            master=self,
            text="適用",
            width=50,
            command=self.rigidity_apply_button_function,
            font=self.fonts,
        )
        self.rigidity_apply_button.place(x=130, y=130)

        # tolerate face errors widget
        self.tolerate_target_face__errors_toggle_button = customtkinter.CTkButton(
            master=self,
            text=tolerate_target_face__errors_text[int(tolerate_target_face__errors)],
            width=175,
            command=self.tolerate_target_face__errors_toggle_button_function,
            font=self.fonts,
        )
        self.tolerate_target_face__errors_toggle_button.place(x=5, y=165)

        # --- log widgets ---
        self.ave_threshold_title = customtkinter.CTkLabel(
            master=self, text="平均 類似度: ", font=self.fonts
        )
        self.ave_threshold_title.place(x=210, y=60)
        self.ave_threshold_text = customtkinter.CTkLabel(
            master=self, text="", font=self.fonts
        )
        self.ave_threshold_text.place(x=325, y=60)

        self.min_threshold_title = customtkinter.CTkLabel(
            master=self, text="最良 類似度: ", font=self.fonts
        )
        self.min_threshold_title.place(x=210, y=90)
        self.min_threshold_text = customtkinter.CTkLabel(
            master=self, text="", font=self.fonts
        )
        self.min_threshold_text.place(x=325, y=90)

        self.max_threshold_title = customtkinter.CTkLabel(
            master=self, text="最悪 類似度: ", font=self.fonts
        )
        self.max_threshold_title.place(x=210, y=120)
        self.max_threshold_text = customtkinter.CTkLabel(
            master=self, text="", font=self.fonts
        )
        self.max_threshold_text.place(x=325, y=120)

        self.last_rigidity_title = customtkinter.CTkLabel(
            master=self, text="合格判定率: ", font=self.fonts
        )
        self.last_rigidity_title.place(x=210, y=150)
        self.last_rigidity_text = customtkinter.CTkLabel(
            master=self, text="", font=self.fonts
        )
        self.last_rigidity_text.place(x=325, y=150)

        self.last_updated_title = customtkinter.CTkLabel(
            master=self, text="最終更新時間: ", font=self.fonts
        )
        self.last_updated_title.place(x=210, y=180)
        self.last_updated_text = customtkinter.CTkLabel(
            master=self, text="", font=self.fonts
        )
        self.last_updated_text.place(x=325, y=180)
        # -------------------

    def apply_button_function(self):
        global debugging
        global limit

        if asyncio.run(windows_hello_authorization()) != 0:
            return  # Windows Security Challenge

        new_limit = self.textbox.get()
        self.textbox.delete(0, len(new_limit))
        if new_limit.isdecimal():
            limit = int(new_limit)
            self.textbox.configure(placeholder_text="動作間隔: " + new_limit + "s")


    def threshold_apply_button_function(self):
        global debugging
        global threshold

        if asyncio.run(windows_hello_authorization()) != 0:
            return  # Windows Security Challenge

        new_threshold = self.threshold_textbox.get()
        self.threshold_textbox.delete(0, len(new_threshold))
        if isinstance(float(new_threshold), float):
            threshold = float(new_threshold)
            self.threshold_textbox.configure(
                placeholder_text="類似度閾値:" + str(threshold)
            )


    def rigidity_apply_button_function(self):
        global debugging
        global rigidity

        if asyncio.run(windows_hello_authorization()) != 0:
            return  # Windows Security Challenge

        new_rigidity = self.rigidity_textbox.get()
        self.rigidity_textbox.delete(0, len(new_rigidity))
        if new_rigidity.isdecimal():
            rigidity = int(new_rigidity)
            self.rigidity_textbox.configure(
                placeholder_text="判定閾値:" + str(rigidity) + "%"
            )


    def tolerate_target_face__errors_toggle_button_function(self):
        global tolerate_target_face__errors
        if asyncio.run(windows_hello_authorization()) != 0:
            return  # Windows Security Challenge
        if tolerate_target_face__errors == True:
            tolerate_target_face__errors = False
        else:
            tolerate_target_face__errors = True
        self.tolerate_target_face__errors_toggle_button.configure(
            text=tolerate_target_face__errors_text[int(tolerate_target_face__errors)]
        )


# --- Global Variables ---
interval = 0
app = App()
# ------------------------


def debugging_point():  # debugging point
    time.sleep(20)
    print("debug")  # SET BREAK POINT HERE


def interval_countup():
    global interval
    global debugging

    while True:
        interval += 1
        time.sleep(1)
        if debugging:
            print(interval)


def interval_observe():  # keyboard input interval observer
    global interval
    global limit
    global debugging
    global your_pics_dir
    global tolerate_target_face__errors

    while True:
        time.sleep(1)
        if interval >= limit:
            windows_lock_state = bool(Process.GetProcessesByName("logonui"))
            if debugging:
                print("lock_state: ", windows_lock_state)
            if windows_lock_state == 1:
                exit_processes()

            interval = -(sys.maxsize - 10)
            if debugging:
                print("Limit exceeded.")
            (
                face_check_result,
                last_rigidity,
                ave_threshold,
                min_threshold,
                max_threshold,
            ) = Main_Authorization.authorization(
                your_pics_dir, capture_pics_dir, rigidity, threshold, debugging
            )
            if face_check_result == 1 or (
                face_check_result == -2 and tolerate_target_face__errors == False
            ):
                interval = 0
                lock_out()
            else:
                interval = 0
                app.last_rigidity_text.configure(text=str(last_rigidity) + "%")
                app.ave_threshold_text.configure(text=str(round(ave_threshold, 5)))
                app.min_threshold_text.configure(text=str(round(min_threshold, 5)))
                app.max_threshold_text.configure(text=str(round(max_threshold, 5)))
                app.last_updated_text.configure(
                    text=datetime.datetime.now().strftime("%H:%M.%S")
                )


def exit_processes():
    global debugging

    config.set("settings", "debugging", str(debugging))
    config.set("settings", "limit", str(limit))
    config.set("settings", "your_pics_dir", str(your_pics_dir))
    config.set(
        "settings", "tolerate_target_face__errors", str(tolerate_target_face__errors)
    )
    config.set("settings", "rigidity", str(rigidity))
    config.set("settings", "threshold", str(threshold))
    with open("./config.ini", "w") as f:
        config.write(f)
    if debugging:
        print("Config.ini Saved")
    try:
        app.destroy()
    except:
        time.sleep(1)
    sys.exit()


def lock_out():  # lock out from windows user session
    if debugging:
        print("Log Off Function Triggered.")
    winsound.Beep(3000, 500)
    subprocess.call("rundll32.exe user32.dll,LockWorkStation", shell=True)
    exit_processes()


async def windows_hello_authorization():  # Windows Security Challenge Function, It calls C#(.NET Framework) DLL from same dir.
    global debugging
    available = await wscu.UserConsentVerifier.check_availability_async()
    if debugging:
        print("wscu:", available)
    if available == wscu.UserConsentVerifierAvailability.AVAILABLE:
        result = await wscu.UserConsentVerifier.request_verification_async(
            "Face Sentinel requires additional authentication."
        )
        print("wscu_result:", result)
        if result == wscu.UserConsentVerificationResult.VERIFIED:
            return 0
            # OK
        else:
            return 1
            # NG
    else:
        return -1
        # Error


def create_menu():
    app.withdraw()

    def show_app():
        app.deiconify()

    def destroy_app():
        if asyncio.run(windows_hello_authorization()) != 0:
            return  # Windows Security Challenge
        exit_processes()

    menu = (item("表示", show_app), item("終了", destroy_app))
    icon = pystray.Icon(
        "name", Image.open("Assets/headandlock.ico"), "Face Sentinel", menu
    )
    icon.run()


def on_closing():
    app.withdraw()


if __name__ == "__main__":
    if debugging:
        debugging_thread = threading.Thread(target=debugging_point)  # debugging point
        debugging_thread.setDaemon(True)
        debugging_thread.start()

    interval_counter = threading.Thread(
        target=interval_countup
    )  # interval count up function
    interval_counter.setDaemon(True)
    interval_counter.start()

    interval_observer = threading.Thread(
        target=interval_observe
    )  # keyboard input interval observe function
    interval_observer.setDaemon(True)
    interval_observer.start()

    create_menu_variable = threading.Thread(
        target=create_menu
    )  # keyboard input interval observe function
    create_menu_variable.setDaemon(True)
    create_menu_variable.start()

    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()
