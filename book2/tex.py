from math import floor
from perlin import Perlin
from interval import Interval
from image import TextureImage
from vec import Point3, Color


__all__ = ["Texture", "SolidColor", "CheckerTexture", "ImageTexture",
           "NoiseTexture"]


class Texture:
    def value(self, u: float, v: float, p: "Point3") -> "Color":
        '''
        Get the color value with the given uv pair or hit point position.

        Args:
            u: The u value of the uv pair, usually for find the pixel from the
                texture image.
            v: The v value of the uv pair.
            p: The hit point.

        Returns:
            Color: The texture color for rendering.

        '''
        pass


class SolidColor(Texture):
    '''
    Pure color texture.

    Attributes:
        albedo: The color of the texture.
        red, green, blue: The color of the texture in RGB format.

    '''

    def __init__(self,
                 albedo: "Color" = None,
                 red: float = 0, green: float = 0, blue: float = 0) -> None:
        if albedo is not None:
            self.albedo = albedo
        elif red != 0 and green != 0 and blue != 0:
            self.albedo = Color(red, green, blue)
        else:
            raise RuntimeError("Bad Initializing")

    def value(self, u: float, v: float, p: "Point3") -> "Color":
        return self.albedo


class CheckerTexture(Texture):
    '''
    The checker texture.

    Attributes:
        scale: The scale of the pattern. The larger the number is, more
            scattered the pattern is.
        even: The texture when the calculated result is even.
        odd: The texture when the calculated result is odd.
        c1: The color when the calculated result is even.
        c2: The color when the calculated result is odd.

    '''

    def __init__(self,
                 scale: float,
                 even: "Texture" = None,
                 odd: "Texture" = None,
                 c1: "Color" = None,
                 c2: "Color" = None) -> None:
        self.inv_scale = 1.0 / scale
        if even is not None and odd is not None:
            self.even = even
            self.odd = odd
        elif c1 is not None and c2 is not None:
            self.even = SolidColor(albedo=c1)
            self.odd = SolidColor(albedo=c2)
        else:
            raise RuntimeError("Bad Initializing")

    def value(self, u: float, v: float, p: "Point3") -> "Color":
        x_int = floor(self.inv_scale * p.x)
        y_int = floor(self.inv_scale * p.y)
        z_int = floor(self.inv_scale * p.z)

        is_even = (x_int + y_int + z_int) % 2 == 0
        return self.even.value(u, v, p) if is_even else self.odd.value(u, v, p)


class ImageTexture(Texture):
    '''
    The image texture.

    Attributes:
        filename: The location of rendered texture image.

    '''

    def __init__(self, filename: str) -> None:
        self.image = TextureImage(filename=filename)

    def value(self, u: float, v: float, p: "Point3") -> "Color":
        if self.image.image_height < 0:
            return Color(0, 1, 1)
        u = Interval(0, 1).clamp(u)
        v = 1.0 - Interval(0, 1).clamp(v)
        i = int(u * self.image.image_width)
        j = int(v * self.image.image_height)
        pixel = self.image.pixel_data(i, j)
        color_scale = 1.0 / 255
        return Color(color_scale * pixel[0],
                     color_scale * pixel[1],
                     color_scale * pixel[2])


class NoiseTexture(Texture):
    '''
    The noise texture (Perlin noise).

    Attributes:
        scale: The intensity of the noise.

    '''

    def __init__(self, scale: float = 1) -> None:
        self.scale = scale

    def value(self, u: float, v: float, p: "Point3") -> "Color":
        noise = Perlin()
        return Color(1, 1, 1) * noise.turb(p, 7)
