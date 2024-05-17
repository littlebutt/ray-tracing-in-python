from PIL import Image

from vec import Color


class TextureImage:

    def __init__(self, filename: str) -> None:
        self.load(filename)
    
    def load(self, filename: str) -> None:
        image = Image.open(filename)
        self.image_height = image.height
        self.image_width = image.width
        self.data = [[0 for i in range(self.image_width)] for j in range(self.image_height)]
        _data = image.load()
        for w in range(self.image_width):
            for h in range(self.image_height):
                r, g, b = _data[w, h]
                self.data[h][w] = (r, g, b)
    
    def pixel_data(self, x: int, y: int) -> "Color":
        x = self.clamp(x, 0, self.image_width)
        y = self.clamp(y, 0, self.image_height)
        return Color(x=self.data[y][x][0], y=self.data[y][x][1], z=self.data[y][x][2])
    
    @staticmethod
    def clamp(x: int, low: int, high: int) -> int:
        if x < low:
            return low
        if x > high:
            return high
        return x


if __name__ == '__main__':
    ti = TextureImage('./earthmap.jpg')
    print(ti.data)




