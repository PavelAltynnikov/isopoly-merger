import os
from functions import *
from merger import Merger

isopoly_dir = get_pictures_dir()
RESULT_PATH = os.path.join(isopoly_dir, 'result')
create_dir(RESULT_PATH)

pictures = get_pictures(isopoly_dir)
legends = get_legends(isopoly_dir)

if not pictures:
    print('В данной папке нет картинок для слияния.')

if not legends:
    print('В данной папке нет файла с легендами в формате "csv"')

if pictures and legends:
    merge_picture = Merger(create_pictures(isopoly_dir, pictures, legends))
    merge_picture.save_image(RESULT_PATH)

input('Для завершения нажмите любую клавишу')
