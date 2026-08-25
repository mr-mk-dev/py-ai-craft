# 01 - Python Fundamentals: Core Syntax & Flow Control

> **Mental Model**:  
> Python is designed to read almost like plain English.  
> Think of code like a **recipe in a cookbook**:  
> * **Variables** hold your ingredients (data).  
> * **Operators & Conditionals** are the decision steps (*"If the oven is hot, bake for 20 minutes"*).  
> * **Loops** are the repetitive actions (*"Stir until smooth"*).

---

## 📑 Table of Contents
1. [Variables & Data Types](#1-variables--data-types)
2. [Formatted Strings (f-strings)](#2-formatted-strings-f-strings)
3. [Conditional Statements (if, elif, else) & Ternary](#3-conditional-statements-if-elif-else--ternary)
4. [For Loops & range()](#4-for-loops--range)
5. [While Loops & Accumulators](#5-while-loops--accumulators)
6. [Loop Control: break and continue](#6-loop-control-break-and-continue)
7. [Summary & Quick Reference Cheat Sheet](#7-summary--quick-reference-cheat-sheet)

---

## 1. Variables & Data Types

In Python, variables store data values without needing complex keyword declarations:

| Data Type | Purpose | Example |
| :--- | :--- | :--- |
| **`int`** | Whole numbers | `age = 21` |
| **`float`** | Decimal numbers | `temperature = 0.7` |
| **`str`** | Text strings | `name = "Manish"` |
| **`bool`** | True or False flags | `is_active = True` |

```python
# Inspecting variable types with type():
model_name = "gpt-4o"
cost = 0.005
tokens = 150

print(type(model_name))  # <class 'str'>
print(type(cost))        # <class 'float'>
print(type(tokens))      # <class 'int'>
```

---

## 2. Formatted Strings (f-strings)

Use **f-strings** (`f"..."`) to inject variables directly into text using curly braces `{}`:

```python
name = "Manish"
role = "AI Engineer"
experience_years = 2

# Clean, readable string interpolation:
print(f"My name is {name}, and I am an {role} with {experience_years} years of experience.")
```

---

## 3. Conditional Statements (`if`, `elif`, `else`) & Ternary

Conditionals allow your program to make decisions:

```python
score = 85

# Standard if/elif/else:
if score >= 90:
    grade = "A"
elif score >= 75:
    grade = "B"
elif score >= 50:
    grade = "C"
else:
    grade = "F"

print(f"Grade: {grade}")

# Ternary One-Liner (condition_if_true if test else condition_if_false):
status = "Adult" if age >= 18 else "Minor"
```

---

## 4. For Loops & `range()`

Use `for` loops to repeat actions a fixed number of times using `range(start, stop, step)`:

```python
# 1. Loop from 1 to 5 (stop is exclusive!):
for i in range(1, 6):
    print(i, end=" ")  # Prints: 1 2 3 4 5
print()

# 2. Loop with step size of 2 (Even numbers from 2 to 10):
for i in range(2, 11, 2):
    print(i, end=" ")  # Prints: 2 4 6 8 10
print()

# 3. Countdown loop (Step of -1):
for i in range(5, 0, -1):
    print(i, end=" ")  # Prints: 5 4 3 2 1
print()
```

---

## 5. While Loops & Accumulators

A `while` loop runs continuously as long as a condition remains `True`:

```python
# Accumulating a total until a condition is met:
total = 0
current = 1

while current <= 5:
    total += current
    current += 1

print(f"Total Sum: {total}")  # Output: 15
```

---

## 6. Loop Control: `break` and `continue`

* **`break`**: Immediately terminates the loop and exits.
* **`continue`**: Skips the rest of the current iteration and jumps to the next one.

```python
# 1. Skip multiples of 3 using continue:
print("Skipping multiples of 3:")
for i in range(1, 10):
    if i % 3 == 0:
        continue  # Skips 3, 6, 9
    print(i, end=" ")
print()

# 2. Stop at first match using break:
print("Searching for first number divisible by 7 and 11:")
for i in range(1, 100):
    if i % 7 == 0 and i % 11 == 0:
        print(f"Found: {i}")  # Prints 77 and stops
        break
```

---

## 7. Summary & Quick Reference Cheat Sheet

| Syntax | Example | Purpose |
| :--- | :--- | :--- |
| **f-string** | `f"Value: {val}"` | Injects variables into string |
| **Ternary** | `"Even" if x % 2 == 0 else "Odd"` | 1-line conditional expression |
| **range()** | `range(1, 11)` | Generates integers from 1 up to 10 |
| **continue** | `if x == 5: continue` | Skips current loop cycle |
| **break** | `if x == 10: break` | Exits loop immediately |

---

## 🚀 Ready to Practice!
Open [01-python-core/01-python-fundamentals/practice.py](file:///home/user2/PythonProject/Python-for-ai-engineering/01-python-core/01-python-fundamentals/practice.py) to review the solutions!
