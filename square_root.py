import math

# determining sqrt(2):
# sqrt(1) < sqrt(2) < sqrt(4)
# 1 < ? < 2

lower_bound = 1.0
upper_bound = 2.0

for _ in range(100):
    delta = upper_bound - lower_bound
    pivot = lower_bound + 0.5 * delta
    print(pivot)
    square = pivot**2

    if square > 2:
        if upper_bound == pivot:
            print("Reached machine precision")
            break
        upper_bound = pivot
    elif square < 2:
        if lower_bound == pivot:
            print("Reached machine precision")
            break
        lower_bound = pivot
    else:
        # might be possible due to float inaccuracies
        break

print(f"Solution:\n{pivot}")
print(f"Reference:\n{math.sqrt(2)}")
