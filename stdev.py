"""
PSEUDO CODE FOR STANDARD DEVIATION

Define CalculateStdDev:
    Input: a list of numbers
    Output: the standard deviation (spread) of the values

    1. Define CalculateMean:
        Input: a list of numbers
        Output: the average value
        a. Set total to zero
        b. Set count to zero
        c. For each number in list:
            i. Add number to total
            ii. Add one to count
        d. Output total divided by count

    2. Set mean to CalculateMean output
    3. Set sum_difference to zero
    4. Set counter to zero
    5. For each number in list:
        a. Set difference to number minus the mean
        b. Multiply difference to itself
        c. Add difference to sum_difference
        d. Add one to counter

    6. Set mean_difference to sum_difference divide by counter
    7. Set standard_deviation to square root of mean_difference
    8. Output standard_deviation
"""

# CODE BELOW

import random

data = [32, 58, 14, 8, 55, 67, 2]
rand_data = random.sample(range(1, 100), 10)


def calculate_mean(num_list):
    total = 0
    for num in num_list:
        total += num
    return total / len(num_list)


def calculate_std_dev(num_list):
    mean = calculate_mean(num_list)
    squares = [(num - mean) ** 2 for num in num_list]
    mean_difference = calculate_mean(squares)
    standard_deviation = mean_difference ** 0.5
    return standard_deviation


std_dev = calculate_std_dev(data)
rand_std_dev = calculate_std_dev(rand_data)
print('List:', data)
print('Standard Deviation:', std_dev)
print('Random List:', rand_data)
print('Random List Standard Deviation:', rand_std_dev)
