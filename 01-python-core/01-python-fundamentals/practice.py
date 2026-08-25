"""
TOPIC 1 — PYTHON FUNDAMENTALS
=============================
Total Questions: 15
"""


# 1. Write a Python program that stores your name, age, and current learning goal in variables and prints them in a formatted sentence.
# Solution:
# name = "Manish Kumar"
# age = 21
# learning_goal = "Become a Production AI Engineer"
#
# print(f"My name is {name}, I am {age} years old, and my current learning goal is to {learning_goal}.")


# 2. Create variables containing an integer, float, string, and boolean. Print their values and their types using type().
# Solution:
# first  = 2334
# second = 234.43
# third = "Manish"
# fourth = True
# print(first , " " ,type(first)," ",second," ",type(second)," ",third," ",type(third)," ",fourth," ",type(fourth))


# 3. Write a program that takes a number and prints whether it is positive, negative, or zero.
# Solution:
# num = int(input("Enter Num : "))
# val = "Positive" if num > 0 else "Negative" if num < 0 else "Zero"
# print(val)


# 4. Write a program that takes a user's age and prints whether the person is a minor, adult, or senior.
# Solution:
# age = int(input("Enter age : "))
# print("Minor" if age < 18 else "Adult" if 10 <= age < 60 else "senior")


# 5. Write a program that takes three numbers and prints the largest number without using max().
# Solution:
# num1 = int(input("Enter number : "))
# num2 = int(input("Enter number : "))
# num3 = int(input("Enter number : "))
# if num1 > num2:
#     if num3 > num1:
#         print("Num 3 is greater")
#     else :
#         print("Num1 is greater")
# else:
#     if num3 > num2:
#         print("Num 3 is grater")
#     else :
#         print("NUm 2 is greater")


# 6. Write a program that checks whether a given number is even or odd.
# Solution:
# num = int(input("Enter Num : "))
# print("Even" if num%2==0 else "Odd")


# 7. Write a program that prints numbers from 1 to 20 using a for loop.
# Solution:
# for i in range(21):
#     print(i)


# 8. Write a program that prints all even numbers between 1 and 50.
# Solution:
# for i in range(2,50,2):
#     print(i)

# 9. Write a program that calculates the sum of numbers from 1 to n using a loop.
# Solution:
# n = int(input("Enter Number : "))
# sum = 0
# for i in range(n+1):
#     sum+= i
# print(sum)


# 10. Write a program that calculates the factorial of a number using a loop.
# Solution:
# n = int(input("Enter val : "))
# fact = 1
# for i in range(2,n+1,1):
#     fact*=i
# print(fact)



# 11. Write a program that prints the multiplication table of a given number from 1 to 10.
# Solution:
# n = int(input("Enter val : "))
# for i in range(1,11):
#     print(n*i)


# 12. Write a program that counts down from 10 to 1 and then prints "Done!".
# Solution:
# for i in range(10,0,-1):
#     print(i)
# print("Done!")


# 13. Write a program that skips multiples of 3 while printing numbers from 1 to 30 using continue.
# Solution:
# for i in range (31):
#    if i%3 != 0 :
#        print(i)


# 14. Write a program that searches numbers from 1 to 100 and stops
# when it finds the first number divisible by both 7 and 11 using break.
# Solution:
# for i in range (1,101) :
#     if i % 7 == 0 and i % 11 == 0 :
#         print(i)
#         break


# 15. Write a small command-line style program that repeatedly accepts numbers
# and keeps adding them until the user enters 0.
# Solution:
# sum = 0
# while True :
#     num = int (input("Enter val : "))
#     if num == 0 :
#         print(sum)
#         break
#     else:
#         sum += num

