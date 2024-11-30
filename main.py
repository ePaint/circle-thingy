from datetime import datetime
from typing import Optional
import matplotlib.pyplot as plt
from settings.models import Vector
from settings.settings import SETTINGS


def plot_points(plotter: plt,
                points: list[list],
                labels: list[str],
                marker: Optional[str] = None,
                marker_color: str = 'black',
                ha: str = 'center',
                va: str = 'bottom',
                label_color: str = 'black'):
    plotter.scatter(*zip(*points), color=marker_color, marker=marker, s=10)
    for i, label in enumerate(labels):
        plotter.text(points[i][0], points[i][1], label, ha=ha, va=va, color=label_color)


def plot_vectors(plotter: plt,
                 vectors: list[Vector],
                 color: str = 'black'):
    for vector in vectors:
        plotter.plot(
            [vector.origin.x, vector.target.x],
            [vector.origin.y, vector.target.y],
            color=color,
            linewidth=0.5
        )


def main():
    VECTORS = SETTINGS.VECTORS
    layer = SETTINGS.STEP_SIZE
    base_points = [[0, 0]]
    base_labels = [f'{layer}/{layer}']
    middle_points = []
    middle_labels = []
    circle_arcs = []
    circle_lines = []

    layer += SETTINGS.STEP_SIZE
    for vector_index, vector in enumerate(VECTORS):
        base_points.append([vector.target.x, vector.target.y])
        base_labels.append(f'{layer}/{layer}')
        next_vector = VECTORS[(vector_index + 1) % len(VECTORS)]
        circle_arcs.append(vector - next_vector)

    for circle_index in range(1, SETTINGS.NUMBER_OF_CIRCLES):
        inner_layer = layer
        layer += SETTINGS.STEP_SIZE

        for vector in VECTORS:
            vector.length += SETTINGS.LENGTH_INCREMENT_PER_CIRCLE
            base_points.append([vector.target.x, vector.target.y])
            base_labels.append(f'{layer}/{layer}')

        for vector_index, vector in enumerate(VECTORS):
            next_vector = VECTORS[(vector_index + 1) % len(VECTORS)]

            combination_vector = next_vector - vector
            inner_layer_label_template = '[1]/[2]'
            if vector_index % 2 == 1:
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

                inner_layer_value += SETTINGS.STEP_SIZE
                inner_layer_label = inner_layer_label_template.replace('[1]', str(inner_layer_value)).replace('[2]', str(inner_layer))
                middle_labels.append(inner_layer_label)

    circle_lines.extend(VECTORS)

    plot_points(plotter=plt,
                points=base_points,
                labels=base_labels,
                marker_color=SETTINGS.MAIN_COLOR,
                label_color=SETTINGS.MAIN_COLOR)
    plot_points(plotter=plt,
                points=middle_points,
                labels=middle_labels,
                marker_color=SETTINGS.SECONDARY_COLOR,
                label_color=SETTINGS.SECONDARY_COLOR)
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

    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    filename = SETTINGS.OUTPUT_FILE_NAME.replace('[timestamp]', timestamp)
    plt.savefig(filename + '.png', dpi=SETTINGS.OUTPUT_DPI)
    plt.show()


if __name__ == '__main__':
    main()
