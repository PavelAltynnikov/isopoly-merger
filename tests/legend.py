from PIL import ImageDraw
from PIL.Image import Image


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
        colors = [
            same_colors[1]
            for same_colors
            in picture_line.getcolors()
            if same_colors[1] not in Legend.uncorrect_colors
        ]

        if len(colors) != len(self._areas):
            raise ColorsDoNotMatchAreasException(self._isopoly_name, colors, self._areas)

        # срез берётся на тот случай если цвет с альфа каналом
        for color, number in zip(colors, self._areas):
            self._color_number_map.update({color[:3]: number})  # type: ignore
            self._number_color_map.update({number: color[:3]})  # type: ignore

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
        if isinstance(other, int):
            return self

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


class ColorsDoNotMatchAreasException(Exception):
    def __init__(self, isopoly_name, colors, numbers):
        super().__init__()
        self._isopoly_name = isopoly_name
        self._colors = colors
        self._numbers = numbers

    def __str__(self):
        return (
            f'Для изополя "{self._isopoly_name}" '
            'не совпадают цвета в легенде и количество чисел в файле csv\n'
            f'цвета: {self._colors}\n'
            f'числа: {self._numbers}'
        )


class LegendNotFoundException(Exception):
    def __init__(self, isopoly_name):
        super().__init__()
        self._isopoly_name = isopoly_name

    def __str__(self):
        return f'Для изополя "{self._isopoly_name}" не найдены данные в файле csv'


if __name__ == '__main__':
    dct1 = {1: 10, 2: 20, 3: 33}
    dct2 = {4: 40, 2: 22, 3: 30}

    for key, value in dct2.items():
        if key in dct1:
            value = max(value, dct1[key])
        dct1.update({key: value})

    print(dct1)
