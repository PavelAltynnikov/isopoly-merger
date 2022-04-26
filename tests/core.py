import os
import sys

from PIL import Image

TEST_FOLDER = os.path.join(os.path.dirname(__file__), 'test pictures')
SRC = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src')
sys.path.append(SRC)
from functions import get_legends
from isopoly import Isopoly, MergedIsopoly

isopolies = [
    Isopoly(Image.open(os.path.join(TEST_FOLDER, file_name)))
    for file_name
    in os.listdir(TEST_FOLDER)
    if file_name.endswith('png')
]

legends_data = get_legends(TEST_FOLDER)

for isopoly in isopolies:
    isopoly.set_data_into_legend(legends_data)
    isopoly.fill_legend()
    print(isopoly._legend)

merged_legend = sum([isopoly._legend for isopoly in isopolies])
print(merged_legend)

merged_isopoly = MergedIsopoly(isopolies[0].size, merged_legend, isopolies)
merged_isopoly.fill()
merged_isopoly.save(os.path.join(TEST_FOLDER, 'result'))
merged_isopoly.show()
