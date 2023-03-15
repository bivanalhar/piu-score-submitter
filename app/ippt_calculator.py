from bisect import bisect_left

# 25 points scale
static_stn = {
    "max_point": 25,
    "tail_jump": 1,
    "centre_jump": 1.5
}

# 50 points scale
run_stn = {
    "max_point": 50,
    "tail_jump": 0.5,
    "centre_jump": 1
}

categories = {
    1: "<= Inter 6 (15 and below)",
    2: "Inter 7/8 (16 and 17)",
    3: "Inter 9/10 (18 and 19)",
    4: "Adv 1/2 (20)",
    5: "Adv 3/4 (21)",
    6: "Adv 5/6/7 (22)",
    7: "Adv 8/9/10 (23)",
    8: ">= Expert 1 (24 and above)",
}

stations = {
    1: "Static (out of 25 pts)",
    2: "Run (out of 50 pts)"
}

def generate_ippt_table(category, station):
    max_point = station["max_point"]
    tail_jump = station["tail_jump"]
    centre_jump = station["centre_jump"]

    # 100% is the maximum EX-Score
    ex_score = 100

    limits = []  # Stores the EX-Score boundary
    values = []  # Stores the resolved IPPT points

    no_of_divisions = max_point + len(categories)
    times_not_drop = len(categories) - category
    for i in range(no_of_divisions):
        limits.append(ex_score)
        values.append(max_point)

        # Calculate the correct limits
        if i < len(categories) - 1 or i >= no_of_divisions - len(categories) - 1:
            ex_score -= tail_jump
        else:
            ex_score -= centre_jump

        # Calculate the correct values
        if times_not_drop:
            times_not_drop -= 1
        else:
            max_point = max(0, max_point - 1)

    return limits, values


def calculate_ippt_score(ex_score, category, stn_enum):
    stn_object = static_stn if stn_enum == 1 else run_stn
    limits, values = generate_ippt_table(category, stn_object)

    # Use binary search
    # Bisect only supports ascending ordered values
    limits.reverse()
    values.reverse()
    index = bisect_left(limits, ex_score)
    return values[index - 1] if index - 1 > 0 else values[index]  # Round down the value


def main():
    print(calculate_ippt_score(82.88, 4, 1))

if __name__ == "__main__":
    main()
