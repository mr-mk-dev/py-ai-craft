"""
==============================================================================
TOPIC 1 — PYTHON FUNDAMENTALS
==============================================================================
Total Questions: 15
Pure Script Solutions (Variables, Conditionals, Loops — No Functions)
"""

# ==============================================================================
# 1. Write a Python program that stores your name, age, and current learning goal
# in variables and prints them in a formatted sentence.
# ==============================================================================
name = "Manish Kumar"
age = 21
learning_goal = "Become a Production AI Engineer"

print(f"My name is {name}, I am {age} years old, and my current learning goal is to {learning_goal}.")


# ==============================================================================
# 2. Create variables containing an integer, float, string, and boolean.
# Print their values and their types using type().
# ==============================================================================
first = 2334
second = 234.43
third = "Manish"
fourth = True

print(f"Integer: {first} | Type: {type(first)}")
print(f"Float  : {second} | Type: {type(second)}")
print(f"String : {third} | Type: {type(third)}")
print(f"Boolean: {fourth} | Type: {type(fourth)}")


# ==============================================================================
# 3. Write a program that takes a number and prints whether it is positive,
# negative, or zero.
# ==============================================================================
num = 15

if num > 0:
    val = "Positive"
elif num < 0:
    val = "Negative"
else:
    val = "Zero"

print(f"The number {num} is {val}.")


# ==============================================================================
# 4. Write a program that takes a user's age and prints whether the person
# is a minor, adult, or senior.
# ==============================================================================
user_age = 21

if user_age < 18:
    category = "Minor"
elif user_age < 60:
    category = "Adult"
else:
    category = "Senior"

print(f"Age {user_age} is categorized as: {category}")


# ==============================================================================
# 5. Write a program that takes three numbers and prints the largest number
# without using max().
# ==============================================================================
num1 = 45
num2 = 89
num3 = 12

if num1 >= num2 and num1 >= num3:
    largest = num1
elif num2 >= num1 and num2 >= num3:
    largest = num2
else:
    largest = num3

print(f"The largest number among ({num1}, {num2}, {num3}) is: {largest}")


# ==============================================================================
# 6. Write a program that checks whether a given number is even or odd.
# ==============================================================================
check_num = 42
result = "Even" if check_num % 2 == 0 else "Odd"
print(f"The number {check_num} is {result}.")


# ==============================================================================
# 7. Write a program that prints numbers from 1 to 20 using a for loop.
# ==============================================================================
print("Numbers from 1 to 20:")
for i in range(1, 21):
    print(i, end=" ")
print()


# ==============================================================================
# 8. Write a program that prints all even numbers between 1 and 50.
# ==============================================================================
print("Even numbers from 1 to 50:")
for i in range(2, 51, 2):
    print(i, end=" ")
print()


# ==============================================================================
# 9. Write a program that calculates the sum of numbers from 1 to n using a loop.
# ==============================================================================
n = 10
total_sum = 0

for i in range(1, n + 1):
    total_sum += i

print(f"The sum of numbers from 1 to {n} is: {total_sum}")


# ==============================================================================
# 10. Write a program that calculates the factorial of a number using a loop.
# ==============================================================================
fact_n = 5
fact = 1

for i in range(2, fact_n + 1):
    fact *= i

print(f"The factorial of {fact_n} is: {fact}")


# ==============================================================================
# 11. Write a program that prints the multiplication table of a given number
# from 1 to 10.
# ==============================================================================
table_num = 7
print(f"--- Multiplication Table for {table_num} ---")
for i in range(1, 11):
    print(f"{table_num} x {i:2d} = {table_num * i}")


# ==============================================================================
# 12. Write a program that counts down from 10 to 1 and then prints 'Done!'.
# ==============================================================================
print("Countdown:")
for i in range(10, 0, -1):
    print(i, end=" -> ")
print("Done!")


# ==============================================================================
# 13. Write a program that skips multiples of 3 while printing numbers from
# 1 to 30 using continue.
# ==============================================================================
print("Numbers 1 to 30 (skipping multiples of 3):")
for i in range(1, 31):
    if i % 3 == 0:
        continue
    print(i, end=" ")
print()


# ==============================================================================
# 14. Write a program that searches numbers from 1 to 100 and stops
# when it finds the first number divisible by both 7 and 11 using break.
# ==============================================================================
for i in range(1, 101):
    if i % 7 == 0 and i % 11 == 0:
        print(f"First number divisible by both 7 and 11 is: {i}")
        break


# ==============================================================================
# 15. Write a small program that repeatedly accepts numbers and keeps adding
# them until 0 is reached.
# ==============================================================================
input_values = [10, 20, 15, 5, 0, 99]
accumulator = 0

for val in input_values:
    if val == 0:
        break
    accumulator += val

print(f"Total accumulated sum until 0: {accumulator}")
