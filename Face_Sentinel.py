from pynput.keyboard import Listener
import time
import threading
import customtkinter


# --- Global Variables ---
interval = 0
debugging = True
limit = 10   # It may be changed by GUI input
# ------------------------



def Debugging_Point():   # debugging point
    time.sleep(20)
    print("debug")   # SET BREAK POINT HERE


def Interval_CountUp():
    global interval
    global debugging

    while True:
        interval += 1
        time.sleep(1)
        if(debugging):
            print(interval)


def onPress(key):   # keylog listener
    global interval
    interval = 0



class App(customtkinter.CTk):   # CustomTKinter (GUI) Class
    def __init__(self):
        super().__init__()
        self.geometry("250x30+"+str(self.winfo_screenwidth()/2)+"+"+str(10))   # Setting form size
        self.attributes("-topmost", 1)   # Display at the front
        self.title("Face Sentinel")









if __name__ == "__main__":
    debugging_thread = threading.Thread(target=Debugging_Point)   # debugging point
    debugging_thread.setDaemon(True)
    debugging_thread.start()

    key_listener= Listener(on_press=onPress)   # keylog listener
    key_listener.setDaemon(True)
    key_listener.start()


    interval_counter= threading.Thread(target=Interval_CountUp)   # interval count up function
    interval_counter.setDaemon(True)
    interval_counter.start()
    
    app = App()
    app.mainloop()