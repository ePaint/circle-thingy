import yaml
from pydantic import BaseModel, Field
from settings.models import Vector


class Settings(BaseModel):
    MAIN_COLOR: str = '#3d85c6'
    SECONDARY_COLOR: str = '#674ea7'
    TERTIARY_COLOR: str = '#434343'
    FONT_SIZE: int = 10
    DOT_SIZE: int = 5
    ROUNDING_PRECISION: int = 4
    BASE_SEED_NUMERATOR: int = 1
    BASE_SEED_DENOMINATOR: int = 1
    NUMBER_OF_CIRCLES: int = 10
    LENGTH_INCREMENT_PER_CIRCLE: float = 1.0
    SHOW_PLOT: bool = True
    OUTPUT_ENABLED: bool = False
    OUTPUT_FOLDER: str = 'output'
    OUTPUT_FILE_NAME: str = 'output_[timestamp]'
    OUTPUT_SIZE_INCHES: float = 10.0
    OUTPUT_DPI: int = 300
    DRAW_CIRCLE_LINES: bool = True
    DRAW_CIRCLE_ARCS: bool = True
    VECTORS: list[Vector] = Field(default_factory=list)


def read_settings():
    with open('settings.yaml', 'r') as file:
        data = yaml.safe_load(file)
        for vector in data['VECTORS']:
            vector['length'] = data['LENGTH_INCREMENT_PER_CIRCLE']
    return Settings(**data)


SETTINGS = read_settings()
