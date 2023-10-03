import tkinter
from tkinter.filedialog import askopenfile

import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import csv
import pyttsx3 as textSpeach
import time
from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import *
import os
import cv2
import sys
from PIL import Image, ImageTk
import numpy
from PIL import Image
import PIL

engine = textSpeach.init()
count = 0
path = 'images'
images = []
personNames = []
myList = os.listdir(r'C:\Users\ADMIN\Desktop\My Projects\Face_Recognition _Attendance_System\Face_Recognition_Project-main\images')

print(myList)
for cu_img in myList:
    current_Img = cv2.imread(f'{path}/{cu_img}')
    images.append(current_Img)

    personNames.append(os.path.splitext(cu_img)[0])
print(personNames)


# def faceEncodings(images):
#     encodeList = []
#     for img in images:
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         encode = face_recognition.face_encodings(img)[0]
#         encodeList.append(encode)
#     return encodeList

def faceEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Detect faces in the image
        face_locations = face_recognition.face_locations(img)
        
        if len(face_locations) > 0:
            encode = face_recognition.face_encodings(img, face_locations)[0]
            encodeList.append(encode)
    return encodeList



def attendance(name):
    with open('Attendance.csv', 'r+') as csvfile:
        myDataList = csvfile.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            time_now = datetime.now()
            tStr = time_now.strftime('%H:%M:%S')
            dStr = time_now.strftime('%d/%m/%Y')
            csvfile.writelines(f'\n{name},{tStr},{dStr}')
            statment = str('welcome to class' + name)
            engine.say(statment)
            engine.runAndWait()


encodeListKnown = faceEncodings(images)
print('All Encodings Complete!!!')

win= Tk()
#Set the geometry of tkinter frame
win.geometry("750x250")
bg = PhotoImage(file = "face2.png")
label1 = Label( win, image = bg)
label1.place(x = 0, y = 0)
#Define a new function to open the window

def mark_win():
    win.destroy()
def open_win():
    passScreen = tk.Tk()
    passScreen.geometry("1200x800")
    passScreen.resizable(width=False, height=False)
    passScreen.title("Password")

    col_names = ("Name", "Time", "Date")
    for i, col_name in enumerate(col_names, start=0):
        tk.Label(passScreen, text=col_name).grid(row=3, column=i, padx=40)

    with open("Attendance.csv", "r", newline="") as passfile:
        reader = csv.reader(passfile)
        data = list(reader)

    entrieslist = []
    for i, row in enumerate(data, start=4):
        entrieslist.append(row[1])
        for col in range(0, 3):
            tk.Label(passScreen, text=row[col]).grid(row=i, column=col)

    passScreen.mainloop()
# def new_candidate():
#     os.system(r'python C:\Users\RAM\PycharmProjects\upload_tkinter\main.py')
#Create a label
Label(win, text= "Welcome to face recognition attendance system" ,font= ('Helvetica 17 bold')).pack(pady=30)
#Create a button to open a New Window
ttk.Button(win, text="Check Attendance", command=open_win).pack()
ttk.Button(win,text = "Mark Attendance" , command= mark_win).pack()
ttk.Button(win,text = "Add Candidate", command= lambda : os.system(r'"C:\Users\ADMIN\Desktop\My Projects\Face_Recognition _Attendance_System\upload_tkinter\main.py"')).pack()

win.mainloop()

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()
    faces = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
    faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)

    facesCurrentFrame = face_recognition.face_locations(faces)
    encodesCurrentFrame = face_recognition.face_encodings(
        faces, facesCurrentFrame)

    for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        # print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            global name
            name = personNames[matchIndex].upper()
            # print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            attendance(name)

    cv2.imshow('camera', frame)
    if cv2.waitKey(1) == 13:
        break

root = Tk()

root.title("Face Recognition Attendance System")
root.geometry('750x250')
bg = PhotoImage(file = "attendance2.png")
label1 = Label(root, image = bg)
lbl1 = Label(root, text="Welcome to Face Recognition Attendance System", font=("Times", "17", "bold italic"))
lbl2 = Label(root, text="Dear " + name + " Your Attendance was recorded successfully!", font=("Times", "15", "bold "))

lbl1.grid(row=0, column=0, sticky=W, pady=2)
lbl2.grid(row=5, column=0, sticky=W, pady=2)
root.wm_attributes('-transparentcolor','white')



def clicked():
    count == 0;
    root.destroy()


# button widget with red color text
# inside
btn = Button(root, text="Done", fg="red", command=clicked)

# set Button grid
btn.grid(column=0, row=500)
root.mainloop()

cap.release()
cv2.destroyAllWindows()
