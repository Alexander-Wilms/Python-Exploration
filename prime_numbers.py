current_candidate = 0

while True:
    current_candidate += 1
    # print(f"Checking if {current_candidate} is prime ", end="")
    is_prime = True
    for possible_divisor in range(2, current_candidate):
        remainder = current_candidate % possible_divisor
        # print(f"{current_candidate} % {possible_divisor} = {remainder}")
        if remainder == 0:
            is_prime = False
    if is_prime:
        # print("✅")
        print(f"{current_candidate}, ", end="", flush=True)
    else:
        # print("❌")
        pass
