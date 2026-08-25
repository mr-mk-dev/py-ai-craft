"""
==============================================================================
TOPIC 1 — PYTHON FUNDAMENTALS
==============================================================================
Total Questions: 15
Verified & Formatted Solutions
"""


# ==============================================================================
# Question 1: Formatted String Variables
# ==============================================================================
# Store your name, age, and current learning goal in variables and print them
# in a formatted sentence.
name = "Manish Kumar"
age = 21
learning_goal = "Become a Production AI Engineer"

print(f"My name is {name}, I am {age} years old, and my goal is to {learning_goal}.")


# ==============================================================================
# Question 2: Data Types & Inspection
# ==============================================================================
# Create variables containing an integer, float, string, and boolean.
# Print their values and types using type().
int_var = 2334
float_var = 234.43
str_var = "Manish"
bool_var = True

print(f"Integer : {int_var} | Type: {type(int_var)}")
print(f"Float   : {float_var} | Type: {type(float_var)}")
print(f"String  : {str_var} | Type: {type(str_var)}")
print(f"Boolean : {bool_var} | Type: {type(bool_var)}")


# ==============================================================================
# Question 3: Number Sign Classifier
# ==============================================================================
# Take a number and print whether it is positive, negative, or zero.
def check_sign(num: int) -> str:
    return "Positive" if num > 0 else "Negative" if num < 0 else "Zero"


# Test with sample value
sample_num = 15
print(f"Number {sample_num} is: {check_sign(sample_num)}")


# ==============================================================================
# Question 4: Age Group Classifier
# ==============================================================================
# Take a user's age and classify into Minor (< 18), Adult (18-59), or Senior (60+).
def classify_age(user_age: int) -> str:
    if user_age < 18:
        return "Minor"
    elif user_age < 60:
        return "Adult"
    else:
        return "Senior"


print(f"Age 21 category: {classify_age(21)}")


# ==============================================================================
# Question 5: Largest of Three Numbers (Without max())
# ==============================================================================
# Find the largest of three numbers using comparison logic.
def find_largest(a: int, b: int, c: int) -> int:
    if a >= b and a >= c:
        return a
    elif b >= a and b >= c:
        return b
    else:
        return c


num1, num2, num3 = 45, 89, 12
print(f"Largest of ({num1}, {num2}, {num3}) is: {find_largest(num1, num2, num3)}")


# ==============================================================================
# Question 6: Even or Odd Checker
# ==============================================================================
def check_even_odd(number: int) -> str:
    return "Even" if number % 2 == 0 else "Odd"


print(f"Number 42 is: {check_even_odd(42)}")


# ==============================================================================
# Question 7: Range Loop (1 to 20)
# ==============================================================================
# Print numbers from 1 to 20 inclusive.
print("Numbers 1 to 20:")
for i in range(1, 21):
    print(i, end=" ")
print()


# ==============================================================================
# Question 8: Even Numbers (1 to 50)
# ==============================================================================
# Print all even numbers between 1 and 50 inclusive.
print("Even numbers 1 to 50:")
for i in range(2, 51, 2):
    print(i, end=" ")
print()


# ==============================================================================
# Question 9: Sum of Numbers from 1 to N
# ==============================================================================
# Calculate the sum of 1 to n using a loop without shadowing built-in sum().
def calculate_sum_to_n(n: int) -> int:
    total_sum = 0
    for i in range(1, n + 1):
        total_sum += i
    return total_sum


print(f"Sum of 1 to 10: {calculate_sum_to_n(10)}")


# ==============================================================================
# Question 10: Factorial Calculation
# ==============================================================================
def calculate_factorial(n: int) -> int:
    fact = 1
    for i in range(2, n + 1):
        fact *= i
    return fact


print(f"Factorial of 5: {calculate_factorial(5)}")


# ==============================================================================
# Question 11: Multiplication Table
# ==============================================================================
def print_multiplication_table(n: int):
    print(f"--- Multiplication Table for {n} ---")
    for i in range(1, 11):
        print(f"{n} x {i:2d} = {n * i}")


print_multiplication_table(7)


# ==============================================================================
# Question 12: Countdown Loop
# ==============================================================================
print("Countdown:")
for i in range(10, 0, -1):
    print(i, end=" -> ")
print("Done!")


# ==============================================================================
# Question 13: Skip Multiples of 3 (Using continue)
# ==============================================================================
# Print numbers 1 to 30, skipping multiples of 3 using continue.
print("Numbers 1 to 30 (skipping multiples of 3):")
for i in range(1, 31):
    if i % 3 == 0:
        continue
    print(i, end=" ")
print()


# ==============================================================================
# Question 14: Search with break
# ==============================================================================
# Search numbers from 1 to 100 and stop at first number divisible by 7 and 11.
for i in range(1, 101):
    if i % 7 == 0 and i % 11 == 0:
        print(f"First number divisible by 7 and 11: {i}")
        break


# ==============================================================================
# Question 15: Cumulative Input Accumulator
# ==============================================================================
# Simulates repeatedly adding numbers until 0 is received.
def simulate_accumulator(inputs: list) -> int:
    total = 0
    for num in inputs:
        if num == 0:
            break
        total += num
    return total


simulated_entries = [10, 25, 15, 0, 99]
print(f"Accumulated sum until 0: {simulate_accumulator(simulated_entries)}")
