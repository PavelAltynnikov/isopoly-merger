import datetime
import os
from typing import Sequence
from PIL import Image
from legend import Legend, LegendDataNotFoundException


class Isopoly:
    def __init__(self, image: Image.Image):
        self._image = image
        self._name = os.path.basename(image.filename)  # type: ignore
        self._legend = Legend(self._name)

    @property
    def size(self):
        return self._image.size

    def set_data_into_legend(self, legends_data: Sequence[Sequence[str]]) -> None:
        """
        Raises:
            LegendNotFoundException: [description]
        """
        for legend_data in legends_data:
            isopoly_name, *areas = legend_data
            areas = [float(number) for number in areas]
            if self._name == isopoly_name:
                self._legend.set_data(areas)
                return
        raise LegendDataNotFoundException(self._name)

    def fill_legend(self):
        left = 0
        upper = Legend.line_on_picture
        right = self._image.size[0]
        lower = Legend.line_on_picture + 1
        legend_line = self._image.crop((left, upper, right, lower))
        self._legend.parse_picture(legend_line)

    def get_rebar_area(self, coordinates: tuple[int, int]) -> float:
        color = self._image.getpixel(coordinates)  # type: tuple[int, int, int]
        return self._legend.get_rebar_area(color[:3])


class MergedIsopoly:
    def __init__(self, size: tuple[int, int], legend: Legend, isopolies: Sequence[Isopoly]):
        self._image = Image.new(mode='RGB', size=size, color=(255, 255, 255))
        self._legend = legend
        self._isopolies = isopolies
        self._name = '{} {}'.format(
            'MergedIsopoly',
            datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        )

    @property
    def size(self):
        return self._image.size

    def fill(self):
        self._fill_isopoly()
        self._delete_old_legend()
        self._legend.print_on_isopoly(self)

    def show(self):
        self._image.show()

    def save(self, path: str):
        self._image.save(os.path.join(path, f"{self._name}.png"))

    def _delete_old_legend(self):
        for x in range(self._image.size[0]):
            for y in range(30):
                self._image.putpixel((x, y), (255, 255, 255, 255))

    def _fill_isopoly(self):
        for x in range(self._image.size[0]):
            for y in range(self._image.size[1]):
                coordinates = (x, y)
                max_area = max([isopoly.get_rebar_area(coordinates) for isopoly in self._isopolies])
                new_color = self._legend.get_color(max_area)
                self._image.putpixel(xy=coordinates, value=new_color)
