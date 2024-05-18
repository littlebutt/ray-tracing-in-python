from random import randint
from typing import List
from vec import Point3
from utils import random_float


class Perlin:

    def __init__(self) -> None:
        self.point_count = 256
        self.randfloat = [random_float() for i in range(self.point_count)]
        self.perm_x = self._perlin_generate_perm()
        self.perm_y = self._perlin_generate_perm()
        self.perm_z = self._perlin_generate_perm()
    
    def noise(self, p: "Point3") -> float:
        i = int(4 * p.x) & 255
        j = int(4 * p.y) & 255 
        k = int(4 * p.z) & 255
        return self.randfloat[self.perm_x[i] ^ self.perm_y[j] ^ self.perm_z[k]]

    def _perlin_generate_perm(self) -> List[int]:
        p = [i for i in range(self.point_count)]
        self._permute(p, self.point_count)
        return p
    

    @staticmethod
    def _permute(p: List[int], n: int):
        for i in range(n - 1, -1, -1):
            target = randint(0, i)
            p[i], p[target] = p[target], p[i]