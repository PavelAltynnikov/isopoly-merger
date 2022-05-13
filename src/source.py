import os
import tkinter
import tkinter.filedialog


def get_pictures_dir():
    tkinter.Tk().withdraw()
    return tkinter.filedialog.askdirectory(mustexist=True)


def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)
