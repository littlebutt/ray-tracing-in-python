from math import fabs, floor
from random import randint
from typing import List
from vec import Point3, Vector3
from utils import random_float, random_vector


class Perlin:

    def __init__(self) -> None:
        self.point_count = 256
        self.randfloat = [random_float() for i in range(self.point_count)]
        self.perm_x = self._perlin_generate_perm()
        self.perm_y = self._perlin_generate_perm()
        self.perm_z = self._perlin_generate_perm()

        self.randvec = [random_vector(-1, 1).unit_vector() for i in range(self.point_count)]

    def noise(self, p: "Point3") -> float:
        u = p.x - floor(p.x)
        v = p.y - floor(p.y)
        w = p.z - floor(p.z)

        i = int(floor(p.x))
        j = int(floor(p.y))
        k = int(floor(p.z))
        c = [[[0, 0] for i in range(2)] for j in range(2)]
        
        for di in range(2):
            for dj in range(2):
                for dk in range(2):
                    c[di][dj][dk] = self.randvec[self.perm_x[(i + di) & 255] ^
                                                 self.perm_y[(j + dj) & 255] ^
                                                 self.perm_z[(k + dk) & 255]]
        return self._perlin_interp(c, u, v, w)
    
    def turb(self, p: "Point3", depth: int) -> float:
        accum = 0.0
        weight = 1.0
        tmp = p

        for i in range(depth):
            accum += weight * self.noise(p)
            weight *= 0.5
            tmp *= 2
        
        return fabs(accum)
    
    def _perlin_generate_perm(self) -> List[int]:
        p = [i for i in range(self.point_count)]
        p = self._permute(p, self.point_count)
        return p
    
    @staticmethod
    def _permute(p: List[int], n: int):
        for i in range(n - 1, -1, -1):
            target = randint(0, i)
            p[i], p[target] = p[target], p[i]
        return p
    
    @staticmethod
    def _perlin_interp(c: List[List[List["Vector3"]]], u: float, v: float, w: float):
        uu = u * u * (3 - 2 * u)
        vv = v * v * (3 - 2 * v)
        ww = w * w * (3 - 2 * w)

        accum = 0.0
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    weight = Vector3(u - i, v - j, w - k)
                    accum += (i * uu + (1-i) * (1-uu)) * (j * vv + (1-j) * (1-vv)) * \
                             (k * ww + (1-k) * (1-ww)) * weight.dot(c[i][j][k]) 
        return accum