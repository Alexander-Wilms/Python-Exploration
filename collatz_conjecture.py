import matplotlib.pyplot as plt


def f(n: int) -> int:
    if n % 2 == 0:
        n = n / 2
    else:
        n = 3 * n + 1

    return n


if __name__ == "__main__":
    x = []
    y = []

    for i in range(1, 10000):
        n = i
        iterations = 0
        while n != 1:
            iterations += 1
            n = f(n)
        x.append(i)
        y.append(iterations)

    _, ax = plt.subplots()
    ax.scatter(x, y, s=5)
    plt.show()
