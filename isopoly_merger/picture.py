import os
from PIL import Image


class Picture(object):
    def __init__(self, file_path, legends_csv):
        self._file_name = os.path.basename(file_path)
        self._image = Image.open(file_path)
        self._length = self._image.size[0]
        self._width = self._image.size[1]
        self._list_legend_nums = self._get_list_legend_nums(legends_csv)
        self._legend = self._make_legend()
        self.dict_nums_coordinates = self._get_nums_coordinates()

    def _get_legend_area(self):
        coord_y_area = 12
        area = self._image.crop((0, coord_y_area, self._length, coord_y_area + 1))
        return area

    def _get_list_legend_nums(self, legends_csv):
        for row in legends_csv:
            if row[0] == self._file_name:
                legend_nums = row[1:]
                return legend_nums
        print('Что-то пошло не так.'
              'Похоже в файле "csv" назначено неправиьное имя файла картинки {}'.format(self._file_name))
        return None

    def _make_legend(self):
        area = self._get_legend_area()
        legend = {}
        counter = 0
        for x in range(area.size[0]):
            color = area.getpixel((x, 0))
            if color not in legend and color != (255, 255, 255) and color != (0, 0, 0):
                legend[color] = self._list_legend_nums[counter]
                counter += 1
        return legend

    def get_legend(self):
        return self._legend

    def get_list_legend_nums(self):
        list_legend_nums = self._list_legend_nums
        for i, num in enumerate(list_legend_nums):
            list_legend_nums[i] = float(num)
        return list_legend_nums

    def get_file_name(self):
        return self._file_name

    def get_length(self):
        return self._length

    def get_width(self):
        return self._width

    def get_image(self):
        return self._image

    def _get_nums_coordinates(self):
        dict_nums_legend = {}
        for x in range(self._length):
            for y in range(self._width):
                coordinates = (x, y)
                color = self._image.getpixel(coordinates)
                if color in self._legend:
                    num = self._legend[color]
                    dict_nums_legend[coordinates] = float(num)
        return dict_nums_legend
