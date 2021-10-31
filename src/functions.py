import os
import csv
import tkinter as tk
from tkinter import filedialog
from picture import Picture


def get_pictures_dir():
    print('Выберите папку с изополями армирования')
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askdirectory()
    print(f'Вы выбрали папку {path}')
    return path


def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def _get_files_by_extensions(path, extension):
    files = []
    for file in os.listdir(path):
        if file.endswith(extension):
            files.append(file)
    return files


def get_pictures(path):
    return _get_files_by_extensions(path, ('.jpg', '.png', '.bmp'))


def get_legends(path):
    legends = []
    files = _get_files_by_extensions(path, '.csv')
    if files:
        with open(os.path.join(path, files[0]), 'r') as data_file:
            legends = [line for line in csv.reader(data_file)]
    return legends


def create_pictures(path, pictures, legends):
    list_obj_pictures = []
    for picture_name in pictures:
        list_obj_pictures.append(Picture(os.path.join(path, picture_name), legends))
    return list_obj_pictures
