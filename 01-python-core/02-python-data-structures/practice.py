"""
TOPIC 2 — PYTHON DATA STRUCTURES
================================
Total Questions: 15
"""

# 1. Create a list of 10 programming languages and print the first, last, and middle elements.
# Solution:
# programming_lan = ["java","python","cpp","perl","javascript","c","c#","assembly","cobalt","ruby"]
# print(programming_lan[0])
# print(programming_lan[len(programming_lan)-1])
# print(programming_lan[len(programming_lan)//2])


# 2. Create a list of numbers and calculate its sum, minimum, and maximum without using sum(), min(), or max().
# Solution:
# num = [12,3,4,345,5,11,212,9990,12,3,4,56,663,2,11,3]
# minVal = 10000
# maxVal = -1
# sumVal = 0
# for i in range(len(num)) :
#     if num[i] > maxVal:
#         maxVal = num[i]
#     if num[i] < minVal :
#         minVal = num[i]
#     sumVal += num[i]
#
# print("Min value : ", minVal , " Max value : ",maxVal," Total Sum : ",sumVal)

# 3. Given a list of numbers, create a new list containing only the even numbers.
# Solution:
# num = [1,3,3454,5,54,34,2,3,2,3,54,5,34,52,23,4,42,85,234,24,14,234,235,34,523,54234,5,2345,234,5,534,5234,534,5]
# evenList = []
# index = 0
# for i in range(len(num)):
#     if num[i] % 2 == 0 :
#         evenList.append(num[i])
#         index+= 1

# print(evenList)


# 4. Given a list of strings, create a new list containing only strings longer than 5 characters.
# Solution:
# str1 = ["Manish", "anu", "Harishit", "2334534", "sdf", "Kumar"]
# str2 = []
# for i in range(len(str1)) :
#     if len(str1[i]) > 5 :
#         str2.append(str1[i])
# print(str2)


# 5. Remove duplicate values from a list while preserving their original order.
# Solution:
# val = [1,3,23,1,323,4,12,2,3,4,5343,32,12,334,23,1,0,234]
# val2 = []
# for item in val :
#     if item not in val2 :
#         val2.append(item)
# print(val2)

# 6. Create a tuple containing information about an AI model such as name, provider, and context window.
# Unpack it into variables.
# Solution:
# ai_model = ("GPT-5", "OpenAI", 272000)
# print(ai_model[0])
# print(ai_model[1])
# print(ai_model[2])


# 7. Create a set of programming technologies and demonstrate adding, removing, and checking membership.
# Solution:
# val = {"java","python","javascript"}
# val.add("docker")
# val.add("jenkins")
# print("python" in val)


# 8. Given two sets of technologies, find their common technologies, technologies unique to each set, and their union.
# Solution:
# set1 = {"java","python","cpp","c#"}
# set2 = {"javascript","python","perl","c#","assembly"}
# print(set1.intersection(set2))
# print(set1.union(set2))


# 9. Create a dictionary representing an AI model with keys such as name, provider, context_window, and cost.
# Read and update its values.
# Solution:
# ai_model = {
#     "name": "chatGpt",
#     "provider": "openai",
#     "context_window": "2m",
#     "cost": "$5/million_token"
# }
# print(ai_model.get("s"))
# ai_model["name"] = "gemini"
# ai_model["provider"] = "google"
# ai_model["context_window"] = "3M"
# ai_model["cost"] = "$5/billion_token"
# print(ai_model)

# 10. Write a program that safely retrieves a value from a dictionary even when the key does not exist.
# Solution:
# user = {
#     "name" : "Manish",
#     "rollNo" : 21,
#     "subject" : "dbms"
# }
# print(user.get("job"))

# 11. Given a dictionary of products and prices, calculate the total price of all products.
# Solution:
# product = {
#     "laptop" : 50000,
#     "mobile" : 12540,
#     "fridge" : 24000,
#     "tv" : 12345
# }
# total = sum(product.values())
# print(total)

# 12. Given a list of words, create a dictionary containing each word and its frequency.
# Solution:
# word_list = ["manish","kumar","ranjeetkumar","smith","anuragh","anjali"]
# list_freq = {}
# for item in word_list :
#     list_freq[item] = len(item)
# print(list_freq)

# 13. Given a list of dictionaries representing users, print the names of users whose age is greater than 25.
# Solution:
# users = [
#     {"name": "Manish", "age": 25},
#     {"name": "Ranjeet", "age": 20},
#     {"name": "Parul", "age": 26},
#     {"name": "Sonu", "age": 52},
#     {"name": "Aman", "age": 42},
# ]
# for user in users :
#     if user.get("age") > 25 :
#         print(user.get("name"))


# 14. Given nested dictionary data representing an API response, extract a deeply nested value safely.
# Solution:
response = {
    "data": {
        "user": {
            "profile": {
                "email": "manish@gmial.com"
            }
        }
    }
}

email = response.get("datas",{}).get("user",{}).get("profile",{}).get("email",{})
print(email)


# 15. Create a small in-memory representation of an LLM API response using dictionaries and lists,
# then extract the model name, response text, token usage, and cost.
# Solution:
api_response = {
    "model": "gpt-4.1",
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": "Hello! How can I help?"
            }
        }
    ],
    "usage": {
        "input_tokens": 12,
        "output_tokens": 8,
        "total_tokens": 20
    },
    "cost": 0.002
}

model_name = api_response.get("model")
response_text = api_response.get("choices")[0].get("message",{}).get("content",{})
token_usage = api_response["usage"]["total_tokens"]
cost = api_response["cost"]

print(model_name)
print(response_text)
print(token_usage)
print(cost)
