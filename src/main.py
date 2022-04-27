import os
import PIL
import source
from isopoly import Isopoly, MergedIsopoly

isopoly_dir = source.get_pictures_dir()
result_path = os.path.join(isopoly_dir, "result")
source.create_dir(result_path)

legends_data = source.parse_legends(isopoly_dir)

isopolies = [
    Isopoly(PIL.Image.open(os.path.join(isopoly_dir, file_name)))
    for file_name in os.listdir(isopoly_dir)
    if file_name.endswith("png")
]

for isopoly in isopolies:
    isopoly.set_data_into_legend(legends_data)
    isopoly.fill_legend()

merged_legend = sum([isopoly._legend for isopoly in isopolies])

merged_isopoly = MergedIsopoly(isopolies[0].size, merged_legend, isopolies)
merged_isopoly.fill()
merged_isopoly.save(result_path)
merged_isopoly.show()

input("Программа завершила свою работу. Нажмите любую клавишу для закрытия окна.")
