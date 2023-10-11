import tkinter as tk
from tkinter import *
import os
import cv2
import sys
from PIL import Image, ImageTk
import numpy
from PIL import Image
import PIL

fileName = os.environ['ALLUSERSPROFILE'] + "\WebcamCap.txt"
cancel = False

def prompt_ok(event = 0):
    global cancel, button, button1, button2
    cancel = True

def saveAndExit(event = 0):
    global prevImg

    if (len(sys.argv) < 2):
        filepath = "New.png"
    else:
        filepath = sys.argv[1]

    print ("Output file to: " + filepath)
    prevImg.save(filepath)
    mainWindow.quit()



def resume(event = 0):
    global button1, button2, button, lmain, cancel

    cancel = False

    button1.place_forget()
    button2.place_forget()

    mainWindow.bind('<Return>', prompt_ok)
    button.place(bordermode=tk.INSIDE, relx=0.5, rely=0.9, anchor=tk.CENTER, width=300, height=50)
    lmain.after(10, show_frame)


try:
    f = open(fileName, 'r')
    camIndex = int(f.readline())
except:
    camIndex = 0

cap = cv2.VideoCapture(camIndex)
capWidth = cap.get(3)
capHeight = cap.get(4)

success, frame = cap.read()

mainWindow = tk.Tk(screenName="Camera Capture")



def retrieve_input():
    inputValue=textBox.get("1.0","end-1c")
    global prevImg

    if (len(sys.argv) < 2):
        filepath = (inputValue+".png")
    else:
        filepath = sys.argv[1]

    print("Output file to: " + filepath)
    prevImg.save(r"C:\Users\ADMIN\Desktop\My Projects\Face_Recognition _Attendance_System\upload_tkinter\Photos\{}".format(filepath))
    # png_img = cv2.imread(r'C:\Users\RAM\PycharmProjects\Face_Recognition_Project-main\images\{}'.format(filepath))
    #
    # # converting to jpg file
    # # saving the jpg file
    # cv2.imwrite(filepath+'.jpg', png_img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    im = Image.open(r"C:\Users\ADMIN\Desktop\My Projects\Face_Recognition _Attendance_System\upload_tkinter\Photos\{}".format(filepath))
    rgb_im = im.convert('RGB')
    filepath2 = (inputValue+".jpg")
    rgb_im.save(r"C:\Users\ADMIN\Desktop\My Projects\Face_Recognition _Attendance_System\Face_Recognition_Project-main\images\{}".format(filepath2))
    mainWindow.quit()
    print(inputValue)

buttonCommit=Button(mainWindow, height=1, width=10, text="Commit",
                    command=lambda: retrieve_input())
buttonCommit.pack()
mainWindow.resizable(width=False, height=False)
mainWindow.bind('<Escape>', lambda e: mainWindow.quit())
lmain = tk.Label(mainWindow, compound=tk.CENTER, anchor=tk.CENTER, relief=tk.RAISED)
lmain.pack()
textBox = Text(mainWindow, height=2, width=10)
textBox.pack()
def show_frame():
    global cancel, prevImg, button

    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

    prevImg = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=prevImg)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    if not cancel:
        lmain.after(10, show_frame)

show_frame()
mainWindow.mainloop()