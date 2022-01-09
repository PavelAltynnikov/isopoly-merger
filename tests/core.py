import os
import sys

from PIL import Image

TEST_PICTURES = os.path.join(os.path.dirname(__file__), 'test pictures')
SRC = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src')
sys.path.append(SRC)
from isopoly import Isopoly, MergedIsopoly


isopolies = [
    Isopoly(Image.open(os.path.join(TEST_PICTURES, file_name)))
    for file_name
    in os.listdir(TEST_PICTURES)
    if file_name.endswith('png')
]

legend = {
    (238, 221, 255): 3.92,
    (255, 255, 147): 7.85,
    (0, 206, 0): 9.58,
    (255, 159, 64): 11.6,
    (164, 164, 0): 14,
    (0, 0, 255): 16.6,
    (255, 0, 255): 19.6,
}

[isopoly.set_legend(legend) for isopoly in isopolies]

merged_legend = {
    3.92: (238, 221, 255),
    7.85: (255, 255, 147),
    9.58: (0, 206, 0),
    11.6: (255, 159, 64),
    14: (164, 164, 0),
    16.6: (0, 0, 255),
    19.6: (255, 0, 255),
    -1: (255, 255, 255)
}

merged_isopoly = MergedIsopoly(isopolies[0].size, merged_legend, isopolies)
merged_isopoly.fill()
merged_isopoly.show()
