import os
import cv2
import tkinter, tkinter.messagebox
import customtkinter
from tkinter import filedialog as fd
from validation import validate_video_file, validate_photo_file, validate_directory

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("500x300")
root.minsize(400, 300)
root.maxsize(400, 300)
root.title("ML project")
root.iconbitmap("hand_sign.ico")


def live_button_function():
    # link to recognitionAllLetters.py
    print("recognitionAllLetters should run")


def video_button_function():
    filename = fd.askopenfilename()

    if not validate_video_file(filename):
        return
    # run the video and save result video

    result_vid = filename  # the new video name

    if view.get() == 'on':
        video = cv2.VideoCapture(filename)
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

    for img_name in os.listdir(dirname):
        validate_photo_file(img_name)
        # save photo with bounding box to another directory

    results_dir = dirname  # the new directory name

    if view.get() == 'on':
        for img_name in os.listdir(results_dir):
            if img_name == 'desktop.ini':
                continue
            img = cv2.imread(results_dir + '\\' + img_name)
            cv2.imshow("Results photo", img)
            cv2.waitKey(0)
        cv2.destroyAllWindows()


def info_button_function():
    tkinter.messagebox.showinfo("Authors", "Course: Introduction to Machine Learning 22/23\n\n"
                                           "Authors: Maciej Radziwił\n\tDawid Mączka\n\t"
                                           "Nikodem Olszowy\n\tMateusz Sudejko\n\t"
                                           "Maciej Saju Sajecki")


frame = customtkinter.CTkFrame(master=root,
                               width=350,
                               height=250,
                               corner_radius=10)
frame.pack(padx=20, pady=20)

label = customtkinter.CTkLabel(master=frame, text="Sign alphabet recognition", font=("Arial", 24))
label.place(relx=0.5, rely=0.05, anchor=tkinter.N)

live_button = customtkinter.CTkButton(master=frame, text="Live recognition", command=live_button_function)
live_button.place(relx=0.5, rely=0.35, anchor=tkinter.CENTER)

video_button = customtkinter.CTkButton(master=frame, text="Video analysis", command=video_button_function)
video_button.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

photo_button = customtkinter.CTkButton(master=frame, text="Photo set analysis", command=photo_button_function)
photo_button.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)

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

root.mainloop()
