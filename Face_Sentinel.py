import sys
import time
import threading
import customtkinter
import subprocess
import clr # Python.net
from pystray import MenuItem as item
import pystray
from PIL import Image, ImageTk


clr.AddReference("WBF_API_ClassLibrary")
import WBF_API_ClassLibrary as auth_api
import Face_Checker




# ------ Configure -------
debugging = True
limit = 100   # It may be changed by GUI input
your_pics_dir = "C:\\FACES\\Known"
tolerate_target_face__errors = False
rigidity = 100
threshold = 0.5
# ------------------------








class App(customtkinter.CTk):   # CustomTKinter (GUI) Class

    def __init__(self):
        super().__init__()
        self.fonts = ("meiryo", 15)
        self.iconbitmap('Assets/headandlock.ico')
        self.geometry("350x120+"+str(self.winfo_screenwidth()/2)+"+"+str(10))   # Setting form size
        # self.attributes("-topmost", 1)   # Display at the front
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

        self.rigidity_textbox = customtkinter.CTkEntry(master=self, placeholder_text="Rigidity:" + str(rigidity) + "%", width=120, font=self.fonts)
        self.rigidity_textbox.place(x=0, y=30)
        self.rigidity_apply_button = customtkinter.CTkButton(master=self, text="Apply", width=50, command=self.rigidity_apply_button_function, font=self.fonts)
        self.rigidity_apply_button.place(x=120, y=30)

        self.threshold_textbox = customtkinter.CTkEntry(master=self, placeholder_text="Threshold:" + str(threshold), width=120, font=self.fonts)
        self.threshold_textbox.place(x=175, y=30)
        self.threshold_apply_button = customtkinter.CTkButton(master=self, text="Apply", width=50, command=self.threshold_apply_button_function, font=self.fonts)
        self.threshold_apply_button.place(x=295, y=30)

        self.last_rigidity_text = customtkinter.CTkLabel(master=self, text="Last Rigidity: ", font=self.fonts)
        self.last_rigidity_text.place(x=0, y=60)

        self.ave_threshold_text = customtkinter.CTkLabel(master=self, text="Ave Threshold: ", font=self.fonts)
        self.ave_threshold_text.place(x=175, y=60)

        self.min_threshold_text = customtkinter.CTkLabel(master=self, text="Min Threshold: ", font=self.fonts)
        self.min_threshold_text.place(x=0, y=90)

        self.max_threshold_text = customtkinter.CTkLabel(master=self, text="Max Threshold: ", font=self.fonts)
        self.max_threshold_text.place(x=175, y=90)



    def apply_button_function(self):
        global debugging
        global limit
        
        if(Windows_Hello_Authorization() != 0): return # Windows Security Challenge

        new_limit = self.textbox.get()
        self.textbox.delete(0, len(new_limit))
        if(new_limit.isdecimal()):
            limit = int(new_limit)
            self.limit_text2.configure(text=str(new_limit))


    def rigidity_apply_button_function(self):
        global debugging
        global rigidity
        
        if(Windows_Hello_Authorization() != 0): return # Windows Security Challenge

        new_rigidity = self.rigidity_textbox.get()
        self.rigidity_textbox.delete(0, len(new_rigidity))
        if(new_rigidity.isdecimal()):
            rigidity = int(new_rigidity)
            self.rigidity_textbox.configure(placeholder_text="Rigidity:" + str(rigidity) + "%")


    def threshold_apply_button_function(self):
        global debugging
        global threshold
        
        if(Windows_Hello_Authorization() != 0): return # Windows Security Challenge

        new_threshold = self.threshold_textbox.get()
        self.threshold_textbox.delete(0, len(new_threshold))
        if(isinstance(float(new_threshold), float)):
            threshold = float(new_threshold)
            self.threshold_textbox.configure(placeholder_text="Threshold:" + str(threshold))










# --- Global Variables ---
interval = 0
app = App()
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



def interval_observe():   # keyboard input interval observer
    global interval
    global limit
    global debugging
    global your_pics_dir
    global tolerate_target_face__errors

    while True:
        time.sleep(1)
        if(interval > limit):
            limit_temp = limit
            limit = sys.maxsize
            if(debugging): print("Limit exceeded.")
            face_check_result, last_rigidity, ave_threshold, min_threshold, max_threshold = Face_Checker.face_check(your_pics_dir, rigidity, threshold, debugging)
            if(face_check_result == 1 or ( face_check_result == -2 and tolerate_target_face__errors == False )) : lock_out()
            else:
                limit = limit_temp
                interval = 0
                app.last_rigidity_text.configure(text="Last Rigidity: " + str(last_rigidity) + "%")
                app.ave_threshold_text.configure(text="Ave Threshold: " + str(ave_threshold))
                app.min_threshold_text.configure(text="Min Threshold: " + str(min_threshold))
                app.max_threshold_text.configure(text="Max Threshold: " + str(max_threshold))





def lock_out():   # lock out from windows user session
    if(debugging) : print("Log Off Function Triggered.")
    subprocess.call('rundll32.exe user32.dll,LockWorkStation', shell=True)
    app.quit()


def Windows_Hello_Authorization(): # Windows Security Challenge Function, It calls C#(.NET Framework) DLL from same dir.
    global debugging
    
    auth = auth_api.WBF_API_Class()
    result = auth.Authorization()

    if(debugging): print("call_auth_result :",result)
    return result


def create_menu():
    app.withdraw()
    def show_app():
        app.deiconify()

    def destroy_app():
        app.destroy()
        
    menu=(item('Show', show_app), item('Quit', destroy_app))
    icon=pystray.Icon("name", Image.open('Assets/headandlock.ico'), "My System Tray Icon", menu)
    icon.run()

    




if __name__ == "__main__":

    if(debugging):
        debugging_thread = threading.Thread(target=Debugging_Point)   # debugging point
        debugging_thread.setDaemon(True)
        debugging_thread.start()


    interval_counter= threading.Thread(target=interval_countup)   # interval count up function
    interval_counter.setDaemon(True)
    interval_counter.start()

    interval_observer= threading.Thread(target=interval_observe)   # keyboard input interval observe function
    interval_observer.setDaemon(True)
    interval_observer.start()

    create_menu_variable= threading.Thread(target=create_menu)   # keyboard input interval observe function
    create_menu_variable.setDaemon(True)
    create_menu_variable.start()
    
    
    
    app.mainloop()