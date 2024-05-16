from math import floor
from vec import Point3, Color


class Texture:

    def value(self, u: float, v: float, p: "Point3") -> "Color":
        pass


class SolidColor(Texture):

    def __init__(self, albedo: "Color"=None, red: float=0, green: float=0, blue: float=0) -> None:
        if albedo is not None:
            self.albedo = albedo
        elif red != 0 and green != 0 and blue !=0:
            self.albedo = Color(red, green, blue)
        else:
           raise RuntimeError("Bad Initializing")

     
    def value(self, u: float, v: float, p: "Point3") -> "Color":
        return self.albedo


class CheckerTexture(Texture):

    def __init__(self, scale: float, even: "Texture"=None, odd: "Texture"=None,
                 c1: "Color"=None, c2: "Color"=None) -> None:
        self.inv_scale = 1.0 / scale
        if even is not None and odd is not None:
            self.even = even
            self.odd = odd
        elif c1 is not None and c2 is not None:
            self.even = SolidColor(albedo=c1)
            self.odd = SolidColor(albedo=c2)
        else:
            raise RuntimeError("Bad Initializing")
    
    def value(self, u: float, v: float, p: Point3) -> Point3:
        x_int = floor(self.inv_scale * p.x)
        y_int = floor(self.inv_scale * p.y)
        z_int = floor(self.inv_scale * p.z)

        is_even = (x_int + y_int + z_int) % 2 == 0
        return self.even.value(u, v, p) if is_even else self.odd.value(u, v, p)