import math
import time
from collections import namedtuple
from dataclasses import dataclass

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import random

RADIUS = 100
IMAGE_SIZE = RADIUS + 1


def point_distance(p1, p2) -> float:
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    return math.sqrt(dx * dx + dy * dy)


@dataclass
class Point:
    x: float
    y: float

    def distance(self, p) -> float:
        return point_distance(self, p)


ORIGIN = Point(0, 0)
TRIANGLE_SIDE = RADIUS * math.sqrt(3)

class Chord:
    p1: Point
    p2: Point
    i1: Point
    i2: Point

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

        rise = p1.y - p2.y
        run = p1.x - p2.x

        # Find the points where the extended line segment would intercept the circle.
        if run == 0:
            x1 = p1.x
            x2 = p2.x
            y1 = math.sqrt((RADIUS * RADIUS) - (x1 * x1))
            y2 = -y1
        else:
            slope = rise / run
            # y = mx + b
            # b = y - mx
            y_intercept = p1.y - (slope * p1.x)

            # Invert the axis to draw the segment.
            # segments.set_data([p[0][0], p[1][0]], [p[0][1], p[1][1]])

            # y = mx + b
            # R*R = x * x + y * y
            # R*R = x^2 + m^2x^2 + 2mxb + b^2
            # 0 = (1 + m^2)x^2 + 2mbx + (b^2 - RADIUS^2)
            a = (slope * slope) + 1
            b = 2 * slope * y_intercept
            c = (y_intercept * y_intercept) - (RADIUS * RADIUS)

            x1 = (-b + math.sqrt(b * b - (4 * a * c))) / (2 * a)
            y1 = slope * x1 + y_intercept
            x2 = (-b - math.sqrt(b * b - (4 * a * c))) / (2 * a)
            y2 = slope * x2 + y_intercept

        self.i1 = Point(x1, y1)
        self.i2 = Point(x2, y2)

    def length(self) -> float:
        return point_distance(self.i1, self.i2)


def main():
    plt.style.use("dark_background")
    plt.rcParams.update({'font.size': 22})

    circle1 = plt.Circle((0, 0), radius=RADIUS, color='white', linewidth=1, fill=False)

    fig, ax = plt.subplots(1, 1, figsize=(20, 10))

    ax.add_patch(circle1)

    plt.xlim([-RADIUS * 1.05, RADIUS * 2])
    plt.ylim([-RADIUS * 1.05, RADIUS * 1.1])
    ax.set_aspect(1)

    inside_points = []
    scatter_plot = ax.scatter([], [], s=50, color="yellow")
    current_chord_render, = ax.plot([], [], ms=3, color="cyan")

    ax.text(RADIUS, RADIUS, f'2 Random points in bounding square', style="italic", color="white")

    chord_text = ax.text(RADIUS * 1.05, 0, f'0.0', style="italic", color="white", multialignment="center", name="Ubuntu")

    points_limit = 6000
    random_points = []
    while len(random_points) < points_limit:
        new_point = Point(random.uniform(-RADIUS, RADIUS), random.uniform(-RADIUS, RADIUS))
        # if new_point.distance(ORIGIN) <= RADIUS:
        random_points.append(new_point)

    random_chords = []
    for i in range(0, len(random_points), 2):
        try:
            random_chords.append(Chord(random_points[i], random_points[i + 1]))
        except ValueError as e:
            # This happens when the line doesn't intersect the circle.
            pass

    def update(frame_num):
        artists = []

        # Visualize only every nth chord
        n = 5
        chord_index = frame_num
        if chord_index < len(random_chords) and chord_index % n == 0:
            print(f"Doing {chord_index}")

            chord = random_chords[chord_index]
            current_chord_render.set_data([chord.i1.x, chord.i2.x], [chord.i1.y, chord.i2.y])
            artists.append(current_chord_render)

            scatter_plot.set_offsets([[chord.p1.x, chord.p1.y], [chord.p2.x, chord.p2.y]])
            artists.append(scatter_plot)

            color = "lightblue" if chord.length() > TRIANGLE_SIDE else "lightcoral"
            c_artist, = plt.plot([chord.i1.x, chord.i2.x], [chord.i1.y, chord.i2.y], linewidth=.2, color=color)

        chord_count = chord_index + 1
        long_chord_count = sum([1 if x.length() > TRIANGLE_SIDE else 0 for x in random_chords[:chord_index + 1]])

        chord_text.set_text(f"{long_chord_count} / {chord_count} = {long_chord_count/chord_count:0.4f}")
        artists.append(chord_text)

        return artists


    anim = animation.FuncAnimation(fig, update, frames=2500, interval=10, repeat=False)

    plt.axis('off')
    # plt.show()

    f = r"random_chords_two_points_in_square.mp4"
    writervideo = animation.FFMpegWriter(fps=30)
    anim.save(f, writer=writervideo)

if __name__ == '__main__':
    main()
