import os
import csv
import tkinter as tk
from tkinter import filedialog


def get_pictures_dir():
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askdirectory(mustexist=True)
    return path


def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def parse_legends(path):
    legends = []
    files = _get_files_by_extensions(path, '.csv')
    if files:
        with open(os.path.join(path, files[0]), 'r') as data_file:
            legends = [line for line in csv.reader(data_file)]
    return legends


def _get_files_by_extensions(path, extension):
    files = []
    for file in os.listdir(path):
        if file.endswith(extension):
            files.append(file)
    return files
