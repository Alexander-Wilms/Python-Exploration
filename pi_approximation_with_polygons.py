import math

import matplotlib.pyplot as plt


def area_of_triangle(height: float, base: float) -> float:
    return height * base / 2


def dist(A: tuple[float], B: tuple[float]) -> float:
    return math.sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2)


def approximate_circle_as_ngon(n, draw=True):
    previous_point_on_circle = (1, 0)

    for i in range(1, n + 1):
        # it's a bit recursive to determine pi using pi instead of a compass and a ruler
        this_point_on_circle_x = math.cos(2 * math.pi / n * i)
        this_point_on_circle_y = math.sin(2 * math.pi / n * i)
        this_point_on_circle = (this_point_on_circle_x, this_point_on_circle_y)
        if i == 1:
            area_of_single_triangle = area_of_triangle(1, dist(previous_point_on_circle, this_point_on_circle))
        if draw:
            axes.add_artist(plt.Polygon([(0, 0), previous_point_on_circle, this_point_on_circle], alpha=0.25))
        previous_point_on_circle = this_point_on_circle

    sum_of_areas_of_triangles = n * area_of_single_triangle
    print(sum_of_areas_of_triangles)


figure, axes = plt.subplots()
cc = plt.Circle((0, 0), 1, alpha=0.25)

axes.set_aspect(1)
axes.add_artist(cc)
plt.xlim([-1, 1])
plt.ylim([-1, 1])

approximate_circle_as_ngon(2000, False)
approximate_circle_as_ngon(10, True)
plt.show()
