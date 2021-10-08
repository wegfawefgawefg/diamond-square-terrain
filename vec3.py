import math 
import random

class Vec3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x, self.y, self.z = x, y, z

    def mag(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def norm(self):
        mag = self.mag()
        if mag > 0:
            return Vec3(
                self.x / mag,
                self.y / mag,
                self.z / mag,
            )
        return self

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return Vec3(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return Vec3(self.x / other, self.y / other, self.x / other)

    def dot(self, vec2):
        return self.x * vec2.x + self.y * vec2.y + self.z * vec2.z

    def cross(self, vec2):
        return Vec3(
            self.y * vec2.z - self.z * vec2.y,
            self.z * vec2.x - self.x * vec2.z,
            self.x * vec2.y - self.y * vec2.x
        )

    def __repr__(self):
        return (self.x, self.y, self.z).__repr__()

    def clone(self):
        return Vec3(self.x, self.y, self.z)

    def clamp(self, low, high):
        return Vec3(
            min(max(self.x, low), high),
            min(max(self.y, low), high),
            min(max(self.z, low), high),
        )

    @classmethod
    def unit(self):
        return Vec3(1, 1, 1)

    @classmethod
    def random(self):
        return Vec3(
            random.random(), 
            random.random(), 
            random.random()
        )

class Mat4:
    def __init__(self, 
            a=[1, 0, 0, 0],
            b=[0, 1, 0, 0],
            c=[0, 0, 1, 0],
            d=[0, 0, 0, 1]
        ) -> None:
        self.m = [a, b, c, d]
    
    def __repr__(self) -> str:
        return self.m.__repr__()

    @classmethod
    def rotate_x(cls, angle: float) -> 'Mat4':
        return Mat4(
            [1, 0, 0, 0],
            [0, math.cos(angle), -math.sin(angle), 0],
            [0, math.sin(angle), math.cos(angle), 0],
            [0, 0, 0, 1],
        )
    
    @classmethod
    def rotate_y(cls, angle: float) -> 'Mat4':
        return Mat4(
            [math.cos(angle), 0, math.sin(angle), 0],
            [0, 1, 0, 0],
            [-math.sin(angle), 0, math.cos(angle), 0],
            [0, 0, 0, 1],
        )

    @classmethod
    def rotate_z(cls, angle: float) -> 'Mat4':
        return Mat4(
            [math.cos(angle), -math.sin(angle), 0, 0],
            [math.sin(angle), math.cos(angle), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        )

    @classmethod
    def rot(cls, x, y, z):
        return Mat4.rotate_x(x) * Mat4.rotate_y(y) * Mat4.rotate_z(z)

    @classmethod
    def scale(cls, x, y, z) -> 'Mat4':
        return Mat4(
            [x, 0, 0, 0],
            [0, y, 0, 0],
            [0, 0, z, 0],
            [0, 0, 0, 1],
        )
    
    @classmethod
    def translate(cls, x: float, y: float, z: float) -> 'Mat4':
        return Mat4(
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1],
        )
    
    def __mul__(self, other):
        if isinstance(other, Vec3):
            return Vec3(
                self.m[0][0] * other.x + self.m[0][1] * other.y + self.m[0][2] * other.z + self.m[0][3],
                self.m[1][0] * other.x + self.m[1][1] * other.y + self.m[1][2] * other.z + self.m[1][3],
                self.m[2][0] * other.x + self.m[2][1] * other.y + self.m[2][2] * other.z + self.m[2][3],
            )
        elif isinstance(other, Mat4):
            return Mat4(
                [
                    self.m[0][0] * other.m[0][0] + self.m[0][1] * other.m[1][0] + self.m[0][2] * other.m[2][0] + self.m[0][3] * other.m[3][0],
                    self.m[0][0] * other.m[0][1] + self.m[0][1] * other.m[1][1] + self.m[0][2] * other.m[2][1] + self.m[0][3] * other.m[3][1],
                    self.m[0][0] * other.m[0][2] + self.m[0][1] * other.m[1][2] + self.m[0][2] * other.m[2][2] + self.m[0][3] * other.m[3][2],
                    self.m[0][0] * other.m[0][3] + self.m[0][1] * other.m[1][3] + self.m[0][2] * other.m[2][3] + self.m[0][3] * other.m[3][3],
                ],
                [
                    self.m[1][0] * other.m[0][0] + self.m[1][1] * other.m[1][0] + self.m[1][2] * other.m[2][0] + self.m[1][3] * other.m[3][0],
                    self.m[1][0] * other.m[0][1] + self.m[1][1] * other.m[1][1] + self.m[1][2] * other.m[2][1] + self.m[1][3] * other.m[3][1],
                    self.m[1][0] * other.m[0][2] + self.m[1][1] * other.m[1][2] + self.m[1][2] * other.m[2][2] + self.m[1][3] * other.m[3][2],
                    self.m[1][0] * other.m[0][3] + self.m[1][1] * other.m[1][3] + self.m[1][2] * other.m[2][3] + self.m[1][3] * other.m[3][3],
                ],
                [
                    self.m[2][0] * other.m[0][0] + self.m[2][1] * other.m[1][0] + self.m[2][2] * other.m[2][0] + self.m[2][3] * other.m[3][0],
                    self.m[2][0] * other.m[0][1] + self.m[2][1] * other.m[1][1] + self.m[2][2] * other.m[2][1] + self.m[2][3] * other.m[3][1],
                    self.m[2][0] * other.m[0][2] + self.m[2][1] * other.m[1][2] + self.m[2][2] * other.m[2][2] + self.m[2][3] * other.m[3][2],
                    self.m[2][0] * other.m[0][3] + self.m[2][1] * other.m[1][3] + self.m[2][2] * other.m[2][3] + self.m[2][3] * other.m[3][3],
                ],
                [
                    self.m[3][0] * other.m[0][0] + self.m[3][1] * other.m[1][0] + self.m[3][2] * other.m[2][0] + self.m[3][3] * other.m[3][0],
                    self.m[3][0] * other.m[0][1] + self.m[3][1] * other.m[1][1] + self.m[3][2] * other.m[2][1] + self.m[3][3] * other.m[3][1],
                    self.m[3][0] * other.m[0][2] + self.m[3][1] * other.m[1][2] + self.m[3][2] * other.m[2][2] + self.m[3][3] * other.m[3][2],
                    self.m[3][0] * other.m[0][3] + self.m[3][1] * other.m[1][3] + self.m[3][2] * other.m[2][3] + self.m[3][3] * other.m[3][3],
                ],
            )
        else:
            raise TypeError(f"Mat4.__mul__: Can't multiply {type(self)} with {type(other)}")

    def __rmul__(self, other):
        return self.__mul__(other)
        

            