from vec import Point3, Color


class Texture:

    def value(self, u: float, v: float, p: "Point3") -> "Color":
        pass


class SolidColor(Texture):

    def __init__(self, albedo: "Color"=None, red: float=0, green: float=0, blue: float=0) -> None:
        if albedo is not None:
            self.albedo = albedo
        if red != 0 and grenn != 0 and blue !=0:
            self.albedo = Color(red, green, blue)
        else:
           raise RuntimeError("Bad Initializing")

     
    def value(self, u: float, v: float, p: "Point3") -> "Color":
        return self.albedo
