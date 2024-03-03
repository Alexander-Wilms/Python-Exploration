import math
import random

import matplotlib.pyplot as plt

figure, axes = plt.subplots()
cc = plt.Circle((0, 0), 1, alpha=0.25)

inside_quarter_circle = 0
number_of_samples = 1000000

for iteration in range(number_of_samples):
    x = random.random()
    y = random.random()

    if iteration % 1000 == 0:
        plt.scatter(x, y, color="#4385b1", s=10)

    radius = math.sqrt(x**2 + y**2)

    if radius <= 1:
        inside_quarter_circle += 1

print(f"A_circle/A_square = {inside_quarter_circle}/{number_of_samples}")

# A_circle = pi*r**2
# pi = A_circle/r**2

circle_area_ratio = inside_quarter_circle / number_of_samples
pi = 2 * 2 * circle_area_ratio / 1**2

print(f"pi: {pi}")


axes.set_aspect(1)
plt.xlim([0, 1])
plt.ylim([0, 1])
axes.add_artist(cc)
plt.title("Determining Pi with the Monte Carlo method")
plt.show()
