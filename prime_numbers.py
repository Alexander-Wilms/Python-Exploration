import contextlib
import math
import os
import time


def trial_devision(upper_limit: int, optimization_level: int) -> list[int]:
    current_prime_candidate = 1
    primes = []

    while current_prime_candidate <= upper_limit:
        print(f"Checking if {current_prime_candidate} is prime")

        match optimization_level:
            case 0:
                upper_divisor_limit = current_prime_candidate

            case 1:
                upper_divisor_limit = math.ceil(math.sqrt(current_prime_candidate))

        possible_divisors = range(2, upper_divisor_limit)

        is_prime = True
        for possible_divisor in possible_divisors:
            remainder = current_prime_candidate % possible_divisor
            print(f"{current_prime_candidate} % {possible_divisor} = {remainder}")
            if not remainder:
                is_prime = False
                break

        if is_prime:
            primes.append(current_prime_candidate)
            status = "✅"
        else:
            status = "❌"

        print(f"{current_prime_candidate}: {status}")

        current_prime_candidate += 1

    print()
    return primes


def profile_performance(function: callable, upper_limit: int, optimization_level: int, expected_biggest_prime_in_range: int) -> None:
    start_time = time.time()

    for i in range(5):
        with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
            primes = function(upper_limit, optimization_level)

    end_time = time.time()
    runtime = end_time - start_time
    print(f"Runtime: {runtime} seconds")

    print(primes[-1])
    assert primes[-1] == expected_biggest_prime_in_range


profile_performance(trial_devision, 10000, 1, 9973)
profile_performance(trial_devision, 10000, 0, 9973)
