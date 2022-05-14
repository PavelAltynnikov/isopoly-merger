import os
from typing import Union
from PIL import ImageDraw
from PIL.Image import Image


def find_legends_data_path(dir_path: str) -> str:
    for file_path in os.listdir(dir_path):
        if file_path.endswith('csv'):
            return os.path.join(dir_path, file_path)
    raise LegendsSourceFileNotFoundException(dir_path)


def parse_legends(legends_file_path: str) -> list[list[str]]:
    with open(legends_file_path, 'r') as file:
        lines = file.readlines()
        if not lines:
            raise LegendsSourceFileIsEmptyException(legends_file_path)

        legends_data = [line.strip().split(',') for line in lines]
        if len(legends_data) == 1:
            raise LegendsSourceFileHasOneLegendException(legends_file_path)

        return legends_data


class Legend:
    line_on_picture = 13
    uncorrect_colors = [(255, 255, 255), (255, 255, 255, 255), (0, 0, 0), (0, 0, 0, 255)]

    def __init__(self, isopoly_name):
        self._isopoly_name = isopoly_name
        self._areas = []
        self._color_number_map = {}
        self._number_color_map = {}

    def set_data(self, data):
        self._areas = data

    def parse_picture(self, picture_line: Image):
        colors = self._find_unique_colors(picture_line)

        if len(colors) != len(self._areas):
            raise ColorsDoNotMatchAreasException(self._isopoly_name, colors, self._areas)

        # срез берётся на тот случай если цвет с альфа каналом
        for color, number in zip(colors, self._areas):
            self._color_number_map.update({color[:3]: number})  # type: ignore
            self._number_color_map.update({number: color[:3]})

    def get_rebar_area(self, color: tuple[int, int, int]) -> float:
        return self._color_number_map.get(color, -1.0)

    def get_color(self, area: float) -> tuple[int, int, int]:
        return self._number_color_map.get(area, (255, 255, 255))

    def print_on_isopoly(self, isopoly):
        legend_length = 50
        legend_height = 20
        base_x = isopoly.size[0] - 130
        base_y = 100
        for number, color in self._number_color_map.items():
            self._print_color_rectangle(
                isopoly._image, color,
                legend_length, legend_height,
                base_x, base_y
            )
            self._print_number(
                isopoly._image, number,
                legend_length,
                base_x, base_y
            )
            base_y += 30

    def _find_unique_colors(self, picture_line: Image) -> list[tuple[int, int, int]]:
        colors = []
        y = 0

        for x in range(picture_line.width):
            color = picture_line.getpixel((x, y))
            if color in Legend.uncorrect_colors or color in colors:
                continue
            colors.append(color)

        return colors

    def _print_color_rectangle(self, image, color, length, height, base_x, base_y):
        for x in range(length):
            for y in range(height):
                image.putpixel((base_x + x, base_y + y), color)

    def _print_number(self, image, number, legend_length, base_x, base_y):
        draw = ImageDraw.Draw(image)
        draw.text(
            (base_x + legend_length + 5, base_y + 3), str(number), fill=(0, 0, 0, 255)
        )

    def __add__(self, other: 'Legend'):
        merged_legend = Legend("merged_legend")
        merged_legend._color_number_map = self._color_number_map.copy()

        for key, value in other._color_number_map.items():
            if key in merged_legend._color_number_map:
                value = max(value, merged_legend._color_number_map[key])
            merged_legend._color_number_map.update({key: value})

        merged_legend._number_color_map = {
            area: color
            for color, area
            in merged_legend._color_number_map.items()
        }

        return merged_legend

    def __radd__(self, other: Union['Legend', int]):
        if other == 0:
            return self
        return self.__add__(other)

    def __str__(self):
        return f'name: {self._isopoly_name} colors: {self._number_color_map}'


class LegendsSourceFileNotFoundException(Exception):
    """Представляет исключение возникшее из-за того,
    что по какой-то причине не удалось найти файл-данных легенд изополей.
    """
    def __init__(self, directory: str):
        super().__init__()
        self.directory = directory


class LegendsSourceFileIsEmptyException(Exception):
    """Представляет исключение возникшее из-за того, что файл-данных легенд пуст."""
    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path


class LegendsSourceFileHasOneLegendException(Exception):
    """Представляет исключение возникшее из-за того,
    что в файле-данных легенд находятся данные для одной легенды.
    """
    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path


class LegendDataNotFoundException(Exception):
    """Представляет исключение возникшее из-за того,
    что не удалось найти данные легенды для определённого изополя.
    """
    def __init__(self, isopoly_name):
        super().__init__()
        self.isopoly_name = isopoly_name


class ColorsDoNotMatchAreasException(Exception):
    """Представляет исключение возникшее из-за того,
    что количество цветов легенды изополя, не совпадает
    с количеством площадей легенды из файла-данных.
    """
    def __init__(self, isopoly_name, colors, numbers):
        super().__init__()
        self.isopoly_name = isopoly_name
        self.colors = colors
        self.numbers = numbers


if __name__ == '__main__':
    dct1 = {1: 10, 2: 20, 3: 33}
    dct2 = {4: 40, 2: 22, 3: 30}

    for key, value in dct2.items():
        if key in dct1:
            value = max(value, dct1[key])
        dct1.update({key: value})

    print(dct1)
