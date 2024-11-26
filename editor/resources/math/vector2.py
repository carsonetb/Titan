import math

class Vector2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def normalize(self):
        length = self.length()
        return Vector2(self.x / length, self.y / length)
    
    def length(self) -> float:
        return math.sqrt(self.x^2 + self.y^2)

    def distance_to(self, to) -> float:
        return math.sqrt((to.x - self.x)^2 + (to.y - self.y)^2)

    def to_angle(self) -> float:
        return math.atan2(self.y, self.x)

    def from_angle(angle: float):
        return Vector2(math.cos(angle), math.sin(angle))
    
    def __eq__(self, value) -> bool:
        if self.x == value.x and self.y == value.y: return True
        return False
    
    def __abs__(self):
        return Vector2(self.x, self.y)
    
    def __add__(self, value):
        return Vector2(self.x + value.x, self.y + value.y)
    
    def __sub__(self, value):
        return Vector2(self.x - value.x, self.y - value.y)
    
    def __mul__(self, value):
        return Vector2(self.x * value.x, self.y * value.y)

    def __mul__(self, value: float):
        return Vector2(self.x * value, self.y * value)
    
    def __floordiv__(self, value):
        return Vector2(self.x // value.x, self.y // value.y)
    
    def __div__(self, value):
        return Vector2(self.x / value.x, self.y / value.y)

    def __div__(self, value: float):
        return Vector2(self.x / value, self.y / value)
    
    
