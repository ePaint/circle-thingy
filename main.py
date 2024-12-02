import ast
from datetime import datetime
from pathlib import Path
from typing import Optional
import matplotlib.pyplot as plt
from settings.models import Vector
from settings.settings import SETTINGS


def plot_points(plotter: plt,
                points: list[list],
                fraction_labels: list[str],
                value_labels: list[str] = None,
                marker: Optional[str] = None,
                marker_color: str = 'black',
                label_color: str = 'black',
                font_family: str = 'sans-serif',
                font_size: int = 10,
                dot_size: int = 10):
    plotter.scatter(*zip(*points), color=marker_color, marker=marker, s=dot_size)
    for i, label in enumerate(fraction_labels):
        plotter.text(points[i][0],
                     points[i][1],
                     label,
                     ha='center',
                     va='bottom',
                     variant='normal',
                     color=label_color,
                     family=font_family,
                     fontsize=font_size)
    if value_labels is None:
        return
    for i, label in enumerate(value_labels):
        plotter.text(points[i][0],
                     points[i][1],
                     label,
                     ha='center',
                     va='top',
                     variant='normal',
                     color=label_color,
                     family=font_family,
                     fontsize=font_size)


def plot_vectors(plotter: plt,
                 vectors: list[Vector],
                 color: str = 'black'):
    for vector in vectors:
        plotter.plot(
            [vector.origin.x, vector.target.x],
            [vector.origin.y, vector.target.y],
            color=color,
            linewidth=0.2
        )


def save_fig(folder: str,
             filename: str,
             dpi: int):
    if SETTINGS.OUTPUT_ENABLED:
        timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        folder = Path(folder)
        filename = filename.replace('[timestamp]', timestamp) + '.png'
        filepath = folder / filename
        plt.savefig(filepath, dpi=dpi)


def main():
    VECTORS = SETTINGS.VECTORS
    layer = SETTINGS.BASE_SEED_DENOMINATOR
    base_points = [[0, 0]]
    base_fraction_labels = [f'{SETTINGS.BASE_SEED_NUMERATOR * layer}/{layer}']
    # base_value_labels = [SETTINGS.BASE_SEED_NUMERATOR]
    middle_points = []
    middle_fraction_labels = []
    middle_value_labels = []
    circle_arcs = []
    circle_lines = []

    layer += SETTINGS.BASE_SEED_DENOMINATOR
    for vector_index, vector in enumerate(VECTORS):
        base_points.append([vector.target.x, vector.target.y])
        base_fraction_labels.append(f'{SETTINGS.BASE_SEED_NUMERATOR * layer}/{layer}')
        # base_value_label = round(SETTINGS.BASE_SEED_NUMERATOR * layer / layer, SETTINGS.ROUNDING_PRECISION)
        # base_value_label = int(base_value_label) if base_value_label.is_integer() else base_value_label
        # base_value_labels.append(base_value_label)
        # base_value_labels.append('')
        next_vector = VECTORS[(vector_index + 1) % len(VECTORS)]
        circle_arcs.append(vector - next_vector)

    for circle_index in range(1, SETTINGS.NUMBER_OF_CIRCLES):
        inner_layer = layer
        layer += SETTINGS.BASE_SEED_DENOMINATOR

        for vector in VECTORS:
            vector.length += SETTINGS.LENGTH_INCREMENT_PER_CIRCLE
            base_points.append([vector.target.x, vector.target.y])
            base_fraction_labels.append(f'{SETTINGS.BASE_SEED_NUMERATOR * layer}/{layer}')
            # base_value_label = round(SETTINGS.BASE_SEED_NUMERATOR * layer / layer, SETTINGS.ROUNDING_PRECISION)
            # base_value_label = int(base_value_label) if base_value_label.is_integer() else base_value_label
            # base_value_labels.append(base_value_label)
            # base_value_labels.append('')

        for vector_index, vector in enumerate(VECTORS):
            next_vector = VECTORS[(vector_index + 1) % len(VECTORS)]

            combination_vector = next_vector - vector
            inner_layer_label_template = '[1]/[2]'

            odd_step = vector_index % 2 == 1
            if odd_step:
                combination_vector = vector - next_vector
                inner_layer_label_template = '[2]/[1]'

            circle_arcs.append(combination_vector.model_copy())
            split_segments = circle_index + 1
            lengths = [combination_vector.length / split_segments] * split_segments
            lengths.pop()

            combination_vector.length = 0
            inner_layer_value = 0
            for length in lengths:
                combination_vector.length += length
                middle_points.append([combination_vector.target.x, combination_vector.target.y])

                inner_layer_value += SETTINGS.BASE_SEED_DENOMINATOR
                if not odd_step:
                    inner_layer_fraction_label = inner_layer_label_template.replace('[1]', str(SETTINGS.BASE_SEED_NUMERATOR*inner_layer_value)).replace('[2]', str(inner_layer))
                else:
                    inner_layer_fraction_label = inner_layer_label_template.replace('[1]', str(inner_layer_value)).replace('[2]', str(SETTINGS.BASE_SEED_NUMERATOR*inner_layer))
                inner_layer_value_label = SETTINGS.BASE_SEED_NUMERATOR * (inner_layer / inner_layer_value if odd_step else inner_layer_value / inner_layer)
                inner_layer_value_label = round(inner_layer_value_label, SETTINGS.ROUNDING_PRECISION)
                inner_layer_value_label = int(inner_layer_value_label) if inner_layer_value_label.is_integer() else inner_layer_value_label
                middle_fraction_labels.append(inner_layer_fraction_label)
                middle_value_labels.append(inner_layer_value_label)

    circle_lines.extend(VECTORS)

    plot_points(plotter=plt,
                points=base_points,
                fraction_labels=base_fraction_labels,
                # value_labels=base_value_labels,
                marker_color=SETTINGS.MAIN_COLOR,
                label_color=SETTINGS.MAIN_COLOR,
                font_size=SETTINGS.FONT_SIZE,
                dot_size=SETTINGS.DOT_SIZE)
    plot_points(plotter=plt,
                points=middle_points,
                fraction_labels=middle_fraction_labels,
                value_labels=middle_value_labels,
                marker_color=SETTINGS.SECONDARY_COLOR,
                label_color=SETTINGS.SECONDARY_COLOR,
                font_size=SETTINGS.FONT_SIZE,
                dot_size=SETTINGS.DOT_SIZE)
    if SETTINGS.DRAW_CIRCLE_ARCS:
        plot_vectors(plotter=plt,
                     vectors=circle_arcs,
                     color=SETTINGS.TERTIARY_COLOR)
    if SETTINGS.DRAW_CIRCLE_LINES:
        plot_vectors(plotter=plt,
                     vectors=circle_lines,
                     color=SETTINGS.TERTIARY_COLOR)

    plt.gca().set_aspect('equal', adjustable='box')
    plt.gcf().set_size_inches(SETTINGS.OUTPUT_SIZE_INCHES, SETTINGS.OUTPUT_SIZE_INCHES)
    plt.tight_layout()

    save_fig(folder=SETTINGS.OUTPUT_FOLDER,
             filename=SETTINGS.OUTPUT_FILE_NAME,
             dpi=SETTINGS.OUTPUT_DPI)

    if SETTINGS.SHOW_PLOT:
        plt.show()


if __name__ == '__main__':
    main()
