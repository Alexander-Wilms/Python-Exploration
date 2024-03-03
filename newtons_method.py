import matplotlib.pyplot as plt
import numpy as np
import sympy as sp


def plot_polynomial(equation, x_range=(-5, 5), num_points=100):
    """
    Plots a SymPy polynomial equation

    Args:
    equation:   A SymPy expression representing the polynomial equation
    x_range:    A tuple representing the minimum and maximum x-values (default: (-5, 5))
    num_points: The number of points to use for plotting the curve (default: 100)
    """

    # Convert SymPy symbols to numpy variables
    x = sp.symbols("x")
    x_np = np.linspace(x_range[0], x_range[1], num_points)

    # Convert SymPy expression to a Python function using lambdify
    y_func = sp.lambdify(x, equation, modules=["numpy"])

    # Calculate y-values
    y_np = y_func(x_np)

    figure, axes = plt.subplots()
    # Create the plot
    plt.plot(x_np, y_np, label=f"{equation}")

    # Add labels and title
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("Plot of a Polynomial Equation")

    # Add legend
    plt.legend()

    # Create thicker lines for x=0 and y=0
    plt.axhline(0, color="black", linewidth=2)  # Thicker horizontal line for y=0
    plt.axvline(0, color="black", linewidth=2)  # Thicker vertical line for x=0

    # Show the plot
    plt.grid(True)
    plt.show()


def newton_iteration(function, derivative, x_n) -> float:
    function_at_x_n = function.subs(x, x_n)
    derivative_at_x_n = derivative.subs(x, x_n)
    x_n_plus_1 = x_n - float(function_at_x_n / derivative_at_x_n)
    return x_n_plus_1


def newton_solve(function, intial_guess) -> float:
    derivative = sp.diff(equation, x)

    x_n = intial_guess
    eps = np.finfo(float).eps

    for iteration in range(20):
        # print(f"Iteration {iteration}")
        x_n_plus_1 = newton_iteration(function, derivative, x_n)
        # print(f"{x_n_plus_1=}")
        if abs(x_n_plus_1 - x_n) <= eps:
            break
        else:
            x_n = x_n_plus_1

    print(f"{x_n=}")
    return x_n


# Define the variable
x = sp.symbols("x")

# Define the quadratic equation
equation = (x + 2) * (x - 1)

print(equation)

# Differentiate the equation
derivative = sp.diff(equation, x)

# Print the derivative
print(derivative)

# Apply Newton's method using educated guesses
newton_solve(equation, -1000)
newton_solve(equation, 1000)

plot_polynomial(equation)
