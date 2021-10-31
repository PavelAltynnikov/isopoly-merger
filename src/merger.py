import os
import datetime
from PIL import Image, ImageDraw, ImageFont


class Merger(object):
    def __init__(self, list_obj_pictures):
        self._file_name = '{} {}'.format('MergeMap', datetime.datetime.now().strftime("%Y-%m-%d_%H-%M"))
        self._list_obj_pictures = list_obj_pictures
        self._length = self._get_min_length()
        self._width = self._get_min_width()
        self._nums_legend = self._create_nums_legend()
        self._legend = self._create_legend()
        self._image = self._create_image()

    def _get_min_length(self):
        list_length = []
        for obj_picture in self._list_obj_pictures:
            list_length.append(obj_picture.get_length())
        return min(list_length) + 150

    def _get_min_width(self):
        list_width = []
        for obj_picture in self._list_obj_pictures:
            list_width.append(obj_picture.get_width())
        return min(list_width)

    def get_length(self):
        return self._length

    def get_width(self):
        return self._width

    def _create_nums_legend(self):
        nums_legend = {}
        for obj_picture in self._list_obj_pictures:
            list_nums = obj_picture.get_list_legend_nums()
            for num in list_nums:
                nums_legend[num] = []
        for x in range(self._length):
            for y in range(self._width):
                coordinates = (x, y)
                list_nums = []
                for obj_picture in self._list_obj_pictures:
                    dict_nums_coordinates = obj_picture.dict_nums_coordinates
                    if coordinates in dict_nums_coordinates:
                        num = dict_nums_coordinates[coordinates]
                        list_nums.append(num)
                if list_nums != []:
                    max_num = max(list_nums)
                    nums_legend[max_num].append(coordinates)
        for key in nums_legend.copy():
            if nums_legend[key] == []:
                nums_legend.pop(key)
        return nums_legend

    def _create_color(self):
        list_colors = [
            (192, 192, 192),
            (255, 0, 0),
            (255, 128, 0),
            (255, 255, 87),
            (0, 255, 70),
            (0, 255, 255),
            (0, 0, 255),
            (192, 0, 255),
            (192, 157, 0),
            (86, 128, 0),
            (229, 161, 218),
            (145, 18, 0),
            (30, 30, 30),
        ]
        for color in list_colors:
            yield color

    def _create_legend(self):
        legend = {}
        creator_colors = self._create_color()
        nums_legend = list(self._nums_legend.keys())
        nums_legend.sort()
        for num in nums_legend:
            color = next(creator_colors)
            legend[num] = color
        return legend

    def _print_color_legend(self, image, color, legend_length, legend_height, base_x, base_y):
        for x in range(legend_length):
            for y in range(legend_height):
                image.putpixel((x + base_x, y + base_y), color)

    def _print_num_legend(self, image, legend_length, base_x, base_y, num):
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("GOST_Common.ttf", 14)
        draw.text((base_x + legend_length + 5, base_y + 3), str(num), font=font, fill=(0, 0, 0, 255))

    def _print_legend(self, image, legend):
        legend_length = 50
        legend_height = 20
        base_x = self._length - 120
        base_y = 100
        list_nums = list(legend.keys())
        list_nums.sort()
        for num in list_nums:
            color = legend[num]
            self._print_color_legend(image=image, color=color, legend_length=legend_length, legend_height=legend_height,
                                     base_x=base_x, base_y=base_y)
            self._print_num_legend(image=image, legend_length=legend_length, base_x=base_x, base_y=base_y, num=num)
            base_y += 30

    def _del_old_legend(self, image):
        for x in range(self._length):
            for y in range(30):
                image.putpixel((x, y), (255, 255, 255, 255))

    def _create_image(self):
        new_image = Image.new('RGBA', (self._length, self._width), 'white')
        nums_legend = self._nums_legend
        legend = self._legend
        for num in nums_legend:
            for coord in nums_legend[num]:
                color = legend[num]
                new_image.putpixel(coord, color)
        self._del_old_legend(image=new_image)
        self._print_legend(image=new_image, legend=legend)
        return new_image

    def save_image(self, path):
        self._image.save(os.path.join(path, self._file_name + '.png'))
        print('Слияние изополей выполнено успешно, результат располагается по адресу', path)
