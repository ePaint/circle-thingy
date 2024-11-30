from math import cos, sin, radians, degrees, atan2, sqrt
from pydantic import BaseModel, model_validator, Field
from settings.models import Point


class Vector(BaseModel):
    origin: Point = Point(x=0.0, y=0.0)
    angle: float = 0.0
    length: float = 1.0
    target: Point = Point(x=0.0, y=0.0)
    angle_in_radians: float = Field(default=0.0, exclude=True)

    @model_validator(mode='after')
    def calculate_angle_in_radians(self):
        super().__setattr__('angle_in_radians', radians(self.angle))
        super().__setattr__('target', Point(
            x=round(self.origin.x + self.length * cos(self.angle_in_radians), 3),
            y=round(self.origin.y + self.length * sin(self.angle_in_radians), 3)
        ))
        return self

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        self.calculate_angle_in_radians()

    # implement vector subtraction
    def __sub__(self, other):
        x = self.target.x - other.target.x
        y = self.target.y - other.target.y
        angle = degrees(atan2(y, x))
        length = round(sqrt(x ** 2 + y ** 2), 3)
        return Vector(
            origin=Point(x=other.target.x, y=other.target.y),
            angle=angle,
            length=length
        )


def vector_length(x, y):
    return (x ** 2 + y ** 2) ** 0.5
