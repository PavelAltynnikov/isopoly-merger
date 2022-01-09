from PIL import Image


class Isopoly:
    def __init__(self, image: Image.Image):
        self._image = image
        self._legend = {}

    @property
    def size(self):
        return self._image.size

    def set_legend(self, data: dict[tuple, int]):
        self._legend = data

    def get_rebar_area(self, coordinates: tuple[int, int]) -> int:
        color = self._image.getpixel(coordinates)
        return self._legend.get(color, -1)


class MergedIsopoly:
    def __init__(self, size, legend, isopolies):
        self._image = Image.new(mode='RGB', size=size, color=(255, 255, 255))
        self._legend = legend
        self._isopolies = isopolies

    def fill(self):
        for x in range(self._image.size[0]):
            for y in range(self._image.size[1]):
                coordinates = (x, y)
                max_area = max([isopoly.get_rebar_area(coordinates) for isopoly in self._isopolies])
                new_color = self._legend[max_area]
                self._image.putpixel(xy=coordinates, value=new_color)

    def show(self):
        self._image.show()
