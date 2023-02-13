from tkinter import *
from tkinter import ttk
import subprocess
import qrcode
import time
import math
import os

# create a new dictionary
dic = []

# define the name of the directory to be created
path = "images/WIFIs"

try:
    os.mkdir(path)
except OSError:
    x = "ff"
    #print ("Creation of the directory %s failed" % path)
else:
    x = "oo"
    #print ("Successfully created the directory %s " % path)
    
# Scan for wifi Name and Passwords
data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
for i in profiles:
    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8').split('\n')
    results = [b.split(":")[1][1:-1]for b in results if "Key Content" in b]
    try:
        # add key(wifi_name) and value(wifi_pass) to the dictionary
        dic.append(i)
        img = qrcode.make("WIFI:S:"+i+";T:WPA;P:"+results[0]+";H:false;;")
        img.save("images/WIFIs/" + i + ".png")
    except IndexError:
        # add key(wifi_name) and value(wifi_pass) to the dictionary
        dic.append(i)
        img = qrcode.make("WIFI:S:"+i+";T:OPEN;P:"+""+";H:false;;")
        img.save("images/WIFIs/" + i + ".png")

#wait for 4 seconds
dic = list(dict.fromkeys(dic))
time.sleep(2)

root = Tk()
root.title('WIFIStealler v1.0')
# root.iconbitmap('D:/Projects/Python/images/icon/icons8-wifi-64.ico')
root.geometry("850x400")

# menu bar
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Refresh", command="")
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About...", command="")
menubar.add_cascade(label="Help", menu=helpmenu)
root.config(menu=menubar)

# Create A Main Frame
main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=1)

# Create A Canvas
my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

# Add A Scrollbar To The Canvas
my_scrollbar = ttk.Scrollbar(
    main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)

# Configure The Canvas
my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(
    scrollregion=my_canvas.bbox("all")))

# Create ANOTHER Frame INSIDE the Canvas
second_frame = Frame(my_canvas)

# Add that New frame To a Window In The Canvas
my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

# My content Here
class Photo:
    def __init__(self, photo_path, i, j):
        self.photo_path = photo_path
        self.wrapper = LabelFrame(second_frame, text=photo_path.replace(
            ".png", "").replace("images/WIFIs/",""), width=200, height=200)
        self.wrapper.grid(row=i, column=j, padx=5, pady=5)
        self.photo_image = PhotoImage(file=photo_path)
        self.photo_image = self.photo_image.subsample(3, 3)
        self.photo_label = Label(self.wrapper, image=self.photo_image)
        self.photo_label.grid(row=i, column=j, padx=5, pady=5)


arr = []
k = 0
length = math.ceil(len(dic)/5)+1
for i in range(1, length):
    for j in range(0, 5):
        # test Photo class
        arr.append(Photo("images/WIFIs/"+dic[k]+".png", i, j))
        k += 1
        if (k == len(dic)):
            break

root.mainloop()
