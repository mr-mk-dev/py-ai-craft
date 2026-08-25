"""
==============================================================================
TOPIC 2 — PYTHON DATA STRUCTURES
==============================================================================
Total Questions: 15
Verified & Formatted Solutions
"""

# ==============================================================================
# Question 1: List Indexing (First, Last, Middle)
# ==============================================================================
# Create a list of 10 programming languages and access first, last, and middle.
languages = [
    "Python", "JavaScript", "TypeScript", "Rust", "Go",
    "Java", "C++", "C#", "Ruby", "Swift"
]

first_elem = languages[0]
last_elem = languages[-1]  # Pythonic negative indexing
middle_elem = languages[len(languages) // 2]

print(f"Languages List: {languages}")
print(f"• First  : {first_elem}")
print(f"• Last   : {last_elem}")
print(f"• Middle : {middle_elem}")


# ==============================================================================
# Question 2: Sum, Min, Max (Without Built-in Functions)
# ==============================================================================
# Calculate sum, min, and max using loop iteration and safe initial values.
numbers = [12, 3, 4, 345, 5, 11, 212, 9990, 12, 3, 4, 56, 663, 2, 11, 3]

# Initialize min and max to the first element to handle any range of numbers
min_val = numbers[0]
max_val = numbers[0]
total_sum = 0

for num in numbers:
    if num < min_val:
        min_val = num
    if num > max_val:
        max_val = num
    total_sum += num

print(f"\nNumbers: {numbers}")
print(f"• Min Value : {min_val}")
print(f"• Max Value : {max_val}")
print(f"• Total Sum : {total_sum}")


# ==============================================================================
# Question 3: Filter Even Numbers
# ==============================================================================
# Given a list of numbers, create a new list containing only even numbers.
raw_numbers = [1, 3, 3454, 5, 54, 34, 2, 3, 2, 3, 54, 5, 34, 52, 23, 4, 42]

# Pythonic List Comprehension:
even_numbers = [n for n in raw_numbers if n % 2 == 0]
print(f"\nFiltered Even Numbers: {even_numbers}")


# ==============================================================================
# Question 4: Filter Strings by Length (> 5 characters)
# ==============================================================================
words = ["Manish", "anu", "Harshit", "OpenAI", "sdf", "Engineering"]
long_words = [w for w in words if len(w) > 5]
print(f"\nWords longer than 5 chars: {long_words}")


# ==============================================================================
# Question 5: Remove Duplicates Preserving Original Order
# ==============================================================================
duplicate_list = [1, 3, 23, 1, 323, 4, 12, 2, 3, 4, 5343, 32, 12, 334, 23, 1, 0, 234]

# Approach 1: Using dict.fromkeys (Fastest & Pythonic in Python 3.7+)
unique_ordered = list(dict.fromkeys(duplicate_list))
print(f"\nUnique elements (ordered): {unique_ordered}")


# ==============================================================================
# Question 6: Tuple Unpacking
# ==============================================================================
# Store AI model metadata in a tuple and unpack into descriptive variables.
ai_model_tuple = ("GPT-4o", "OpenAI", 128000)

# Proper Tuple Unpacking:
model_name, provider, context_window = ai_model_tuple
print(f"\nTuple Unpacked -> Model: {model_name} | Provider: {provider} | Context: {context_window} tokens")


# ==============================================================================
# Question 7: Set Operations (Add, Remove, Membership)
# ==============================================================================
technologies = {"Python", "FastAPI", "Docker"}

# 1. Add elements
technologies.add("PostgreSQL")
technologies.add("Redis")

# 2. Remove element safely
technologies.discard("Docker")  # discard avoids KeyError if item doesn't exist

# 3. Check membership
has_python = "Python" in technologies

print(f"\nTechnologies Set: {technologies}")
print(f"• Is 'Python' in set? {has_python}")
print(f"• Is 'Docker' in set? {'Docker' in technologies}")


# ==============================================================================
# Question 8: Set Comparisons (Intersection, Union, Difference)
# ==============================================================================
stack_a = {"Python", "FastAPI", "Docker", "PostgreSQL"}
stack_b = {"Python", "Node.js", "Docker", "MongoDB", "Kubernetes"}

common_tech = stack_a.intersection(stack_b)         # In both
all_tech = stack_a.union(stack_b)                   # In either
unique_to_a = stack_a.difference(stack_b)           # Only in stack_a
unique_to_b = stack_b.difference(stack_a)           # Only in stack_b

print(f"\nStack A: {stack_a}")
print(f"Stack B: {stack_b}")
print(f"• Common (Intersection) : {common_tech}")
print(f"• All Combined (Union)   : {all_tech}")
print(f"• Unique to Stack A      : {unique_to_a}")
print(f"• Unique to Stack B      : {unique_to_b}")


# ==============================================================================
# Question 9: Dictionary Manipulation
# ==============================================================================
ai_model_dict = {
    "name": "Claude-3.5-Sonnet",
    "provider": "Anthropic",
    "context_window": 200000,
    "cost_per_m_input": 3.00,
}

# Read value safely
print(f"\nInitial Provider: {ai_model_dict.get('provider')}")

# Update values
ai_model_dict["context_window"] = 250000
ai_model_dict["supports_vision"] = True

print(f"Updated AI Model Dict: {ai_model_dict}")


# ==============================================================================
# Question 10: Safe Key Retrieval with Defaults
# ==============================================================================
user_profile = {
    "name": "Manish",
    "role": "AI Engineer",
    "preferred_language": "Python",
}

# Access existing and non-existing keys safely with custom default fallbacks
user_role = user_profile.get("role", "General Developer")
user_salary = user_profile.get("salary", "Confidential / Not Disclosed")

print(f"\nUser Role   : {user_role}")
print(f"User Salary : {user_salary}")


# ==============================================================================
# Question 11: Total Price Calculation from Dictionary
# ==============================================================================
catalog = {
    "Laptop": 1200,
    "Mechanical Keyboard": 150,
    "4K Monitor": 450,
    "USB-C Dock": 80,
}

total_price = sum(catalog.values())
print(f"\nTotal Catalog Price: ${total_price}")


# ==============================================================================
# Question 12: Word Frequency Counter
# ==============================================================================
# Calculate how many times each word appears in the list.
corpus = ["ai", "python", "engineer", "ai", "model", "python", "ai", "agent"]

word_freq = {}
for word in corpus:
    word_freq[word] = word_freq.get(word, 0) + 1

print(f"\nWord List: {corpus}")
print(f"Word Frequencies: {word_freq}")


# ==============================================================================
# Question 13: Filter Complex List of Dicts
# ==============================================================================
users_list = [
    {"name": "Manish", "age": 21, "active": True},
    {"name": "Ranjeet", "age": 20, "active": False},
    {"name": "Parul", "age": 26, "active": True},
    {"name": "Sonu", "age": 52, "active": True},
    {"name": "Aman", "age": 42, "active": False},
]

users_over_25 = [u["name"] for u in users_list if u.get("age", 0) > 25]
print(f"\nUsers older than 25: {users_over_25}")


# ==============================================================================
# Question 14: Safe Extraction from Deeply Nested API Response
# ==============================================================================
nested_api_response = {
    "status": "success",
    "data": {
        "user": {
            "profile": {
                "email": "manish@example.com",
                "tier": "pro",
            }
        }
    }
}

# Chained safe extraction preventing KeyError / AttributeError
user_email = (
    nested_api_response.get("data", {})
    .get("user", {})
    .get("profile", {})
    .get("email", "email_not_provided")
)

missing_field = (
    nested_api_response.get("data", {})
    .get("organization", {})
    .get("billing", {})
    .get("card_last4", "no_card_found")
)

print(f"\nSafely Extracted Email: {user_email}")
print(f"Safely Handled Missing Field: {missing_field}")


# ==============================================================================
# Question 15: Mock LLM API Response Parsing
# ==============================================================================
mock_llm_response = {
    "id": "chatcmpl-9901",
    "model": "gpt-4o-2024-08-06",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "A Large Language Model predicts text sequentially using subwords.",
            },
            "finish_reason": "stop",
        }
    ],
    "usage": {
        "prompt_tokens": 15,
        "completion_tokens": 12,
        "total_tokens": 27,
    },
    "estimated_cost_usd": 0.00015,
}

# Extraction
extracted_model = mock_llm_response.get("model", "unknown")
extracted_content = (
    mock_llm_response.get("choices", [{}])[0]
    .get("message", {})
    .get("content", "")
)
extracted_tokens = mock_llm_response.get("usage", {}).get("total_tokens", 0)
extracted_cost = mock_llm_response.get("estimated_cost_usd", 0.0)

print(f"\n--- Parsed LLM API Response ---")
print(f"• Model       : {extracted_model}")
print(f"• Content     : {extracted_content}")
print(f"• Total Tokens: {extracted_tokens}")
print(f"• Cost (USD)  : ${extracted_cost:.5f}")
