import math
import time

import numpy as np
import pygame


class Complex:
    def __init__(self, real: float = 0, imaginary: float = 0):
        self.real = real
        self.imaginary = imaginary

    def __str__(self):
        return f"{self.real} + {self.imaginary} i"

    def __add__(self, other):
        if not isinstance(other, Complex):
            other = Complex(other)
        return Complex(self.real + other.real, self.imaginary + other.imaginary)

    def __sub__(self, other):
        if not isinstance(other, Complex):
            other = Complex(other)
        return Complex(self.real - other.real, self.imaginary - other.imaginary)

    def __rsub__(self, other):
        return self.__sub__(other)

    # Required for int + Complex to work
    # https://discuss.python.org/t/how-to-overload-add-method-in-a-self-made-class-to-sum-multiple-objects-of-the-class/40543/4
    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        if not isinstance(other, Complex):
            other = Complex(other)
        return Complex(self.real * other.real - self.imaginary * other.imaginary, self.real * other.imaginary + self.imaginary * other.real)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __pow__(self, other):
        result = self
        for i in range(other - 1):
            result *= result
        return result

    def magnitude(self):
        return math.sqrt(self.real**2 + self.imaginary**2)


def print_complex_plane(array: np.ndarray):
    shape = array.shape
    for x in range(shape[0]):
        for y in range(shape[1]):
            print(array[x, y], end=" ")
        print()


def within_set(x: float, y: float) -> float:
    z = Complex(0, 0)
    c = Complex(x, y)
    # print(f"z:   {z}")
    # print(f"c:   {c}")
    for iteration in range(100):
        z = z**2 + c
        if z.magnitude() > 2:
            break
        # print(f"Iteration {iteration}: {z}")

    # mag = z.magnitude()
    # print(f"{z} -> {mag}")
    return math.log(iteration)


z = Complex(3, 6)
print(z)
print(z + 1)
print(z**2)
print(z**2 + 1)

within_set(-1, 0)

number_of_samples = 500
x_samples = np.linspace(-1.5, 0.5, number_of_samples)
y_samples = np.linspace(-1, 1, number_of_samples)

complex_plane: np.ndarray = np.ndarray((number_of_samples, number_of_samples))

t1 = time.perf_counter()
for x_idx in range(number_of_samples):
    x = x_samples[x_idx]
    for y_idx in range(number_of_samples):
        y = y_samples[y_idx]
        complex_plane[x_idx, y_idx] = within_set(x, y)
print(f"Time to calculate set: {time.perf_counter() - t1} s")

max = np.max(complex_plane)
complex_plane = complex_plane * 255 / max

pygame.init()
n_x_samples = number_of_samples
n_y_samples = number_of_samples
pixel_scaling_factor = 500 / number_of_samples
display_width = pixel_scaling_factor * n_x_samples
display_height = pixel_scaling_factor * n_y_samples

display_surface = pygame.display.set_mode((display_width, display_height), 0, 64)
image = pygame.Surface((n_x_samples, n_y_samples))
pygame.surfarray.blit_array(image, complex_plane)
image_scaled = pygame.transform.scale(image, (display_width, display_height))
display_surface.blit(image_scaled, (0, 0))

quit = False
while not quit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
    pygame.display.update()
