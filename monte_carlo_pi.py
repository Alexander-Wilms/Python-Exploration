import math
import random

inside_quarter_circle = 0
number_of_samples = 10000000

for iteration in range(number_of_samples):
    x = random.random()
    y = random.random()

    radius = math.sqrt(x**2 + y**2)

    if radius <= 1:
        inside_quarter_circle += 1

print(f"A_circle/A_square = {inside_quarter_circle}/{number_of_samples}")

# A_circle = pi*r**2
# pi = A_circle/r**2

circle_area_ratio = inside_quarter_circle / number_of_samples
pi = 2 * 2 * circle_area_ratio / 1**2

print(f"pi: {pi}")
