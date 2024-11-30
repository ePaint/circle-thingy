from pydantic import BaseModel


class Point(BaseModel):
    x: float = 0.0
    y: float = 0.0

    def get_coordinates(self):
        return self.x, self.y
