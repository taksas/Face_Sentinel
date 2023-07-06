from pynput.keyboard import Listener
import time
import threading
import customtkinter
import subprocess

# --- Global Variables ---
interval = 0
debugging = False
limit = 3   # It may be changed by GUI input
# ------------------------



def Debugging_Point():   # debugging point
    time.sleep(20)
    print("debug")   # SET BREAK POINT HERE


def interval_countup():
    global interval
    global debugging

    while True:
        interval += 1
        time.sleep(1)
        if(debugging): print(interval)


def onPress(key):   # keylog listener
    global interval
    interval = 0


def interval_observe():   # keyboard input interval observer
    global interval
    global limit
    while True:
        time.sleep(1)
        if(interval > limit):
            if(debugging): print("Limit exceeded.")
            face_check()



def face_check():
    log_off()


def log_off():
    global app_exit
    if(debugging) : print("Log Off Function Triggered.")
    else:
        subprocess.check_output('rundll32.exe user32.dll,LockWorkStation', shell=True)
    app.quit()



class App(customtkinter.CTk):   # CustomTKinter (GUI) Class
    def __init__(self):
        super().__init__()
        self.fonts = ("meiryo", 15)
        self.geometry("350x30+"+str(self.winfo_screenwidth()/2)+"+"+str(10))   # Setting form size
        self.attributes("-topmost", 1)   # Display at the front
        self.title("Face Sentinel")
        self.setup_form()   # setup form

    def setup_form(self):
        global limit
        self.textbox = customtkinter.CTkEntry(master=self, placeholder_text="Interval Limit(sec)", width=150, font=self.fonts)
        self.textbox.place(x=0, y=0)
        self.button = customtkinter.CTkButton(master=self, text="Apply", width=70, command=self.apply_button_function, font=self.fonts)
        self.button.place(x=155, y=0)

        self.limit_text1 = customtkinter.CTkLabel(master=self, text="Limit: ", font=self.fonts)
        self.limit_text1.place(x=250, y=0)
        self.limit_text2 = customtkinter.CTkLabel(master=self, text=str(limit), font=self.fonts)
        self.limit_text2.place(x=300, y=0)
    
    def apply_button_function(self):
        global limit
        new_limit = self.textbox.get()
        self.textbox.delete(0, len(new_limit))
        if(new_limit.isdecimal()):
            limit = int(new_limit)
            self.limit_text2.configure(text=str(new_limit))




if __name__ == "__main__":
    global app
    debugging_thread = threading.Thread(target=Debugging_Point)   # debugging point
    debugging_thread.setDaemon(True)
    debugging_thread.start()

    key_listener= Listener(on_press=onPress)   # keylog listener
    key_listener.setDaemon(True)
    key_listener.start()


    interval_counter= threading.Thread(target=interval_countup)   # interval count up function
    interval_counter.setDaemon(True)
    interval_counter.start()

    interval_observer= threading.Thread(target=interval_observe)   # keyboard input interval observe function
    interval_observer.setDaemon(True)
    interval_observer.start()
    
    app = App()
    app.mainloop()