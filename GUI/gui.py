import os
import cv2
import tkinter, tkinter.messagebox
import customtkinter
from tkinter import filedialog as fd
from GUI.validation import validate_video_file, validate_photo_file, validate_directory
import recognition.py_scripts.recognitionAllLetters as recognise

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("500x300")
root.minsize(400, 300)
root.maxsize(400, 300)
root.title("ML project")
root.iconbitmap("GUI/hand_sign.ico")


def live_button_function():
    # link to recognitionAllLetters.py
    recognise.start_recognition_live(is_abc())


def video_button_function():
    filename = fd.askopenfilename()

    if not validate_video_file(filename):
        return
    # run the video and save result video
    result_vid = recognise.start_recognition_video(filename, is_abc())

    if view.get() == 'on':
        video = cv2.VideoCapture(result_vid)
        if not video.isOpened():
            print("Error opening video file")

        while video.isOpened():
            ret, frame1 = video.read()
            if ret:
                cv2.imshow('Frame', frame1)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                break
        video.release()
        cv2.destroyAllWindows()


def photo_button_function():
    dirname = fd.askdirectory()

    if not validate_directory(dirname):
        return
    if not os.path.exists(dirname + '/results'):
        os.mkdir(dirname + '/results')
    for img_name in os.listdir(dirname):
        if not validate_photo_file(img_name):
            continue
        photo_res = recognise.start_recognition_photo(dirname + '/' + img_name, is_abc())
        cv2.imwrite(dirname + '/results/' + img_name, photo_res)
        # save photo with bounding box to another directory

    if view.get() == 'on':
        for img_name in os.listdir(dirname + '/results'):
            if img_name == 'desktop.ini':
                continue
            img = cv2.imread(dirname + '/results/' + img_name)
            cv2.imshow("Results photo", img)
            cv2.waitKey(0)
        cv2.destroyAllWindows()


def is_abc():
    return basic.get() == 'on'


def info_button_function():
    tkinter.messagebox.showinfo("Authors", "Course: Introduction to Machine Learning 22/23\n\n"
                                           "Authors: Maciej Radziwiłł\n\tDawid Mączka\n\t"
                                           "Nikodem Olszowy\n\tMateusz Sudejko\n\t"
                                           "Maciej Saju Sajecki")


def start_gui():
    root.mainloop()


frame = customtkinter.CTkFrame(master=root,
                               width=350,
                               height=250,
                               corner_radius=10)
frame.pack(padx=20, pady=20)

label = customtkinter.CTkLabel(master=frame, text="Sign alphabet recognition", font=("Arial", 24))
label.place(relx=0.5, rely=0.05, anchor=tkinter.N)

live_button = customtkinter.CTkButton(master=frame, text="Live recognition", command=live_button_function)
live_button.place(relx=0.5, rely=0.30, anchor=tkinter.CENTER)

video_button = customtkinter.CTkButton(master=frame, text="Video analysis", command=video_button_function)
video_button.place(relx=0.5, rely=0.50, anchor=tkinter.CENTER)

photo_button = customtkinter.CTkButton(master=frame, text="Photo set analysis", command=photo_button_function)
photo_button.place(relx=0.5, rely=0.70, anchor=tkinter.CENTER)

button = customtkinter.CTkButton(master=frame,
                                 width=20,
                                 height=20,
                                 border_width=1,
                                 corner_radius=8,
                                 text="i",
                                 fg_color="transparent",
                                 border_color="white",
                                 hover_color="gray",
                                 command=info_button_function)
button.place(relx=0.93, rely=0.91, anchor=tkinter.CENTER)

view = tkinter.StringVar(master=frame, value="off")

switch_1 = customtkinter.CTkSwitch(master=frame, text="view non-live results",
                                   variable=view, onvalue="on", offvalue="off")
switch_1.place(relx=0.25, rely=0.91, anchor=tkinter.CENTER)

basic = tkinter.StringVar(master=frame, value="on")

switch_2 = customtkinter.CTkSwitch(master=frame, text="basic",
                                   variable=basic, onvalue="on", offvalue="off")
switch_2.place(relx=0.7, rely=0.91, anchor=tkinter.CENTER)

root.mainloop()
