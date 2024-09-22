import pydantic
from marvin_ai_clone import classify, extract, generate, define, spellCheck
from marvin_ai_with_dspy import classify_dspy, extract_dspy, spellCheck_dspy
import json
# Test cases:

# TODO: Use Co-star, refer to Marvin source code

print(f"TESTING METHOD: classify\nTEXT: Reset my password\nLABELS: ['account issue', 'general inquiry']")
print("\n")
print(f"MANUAL PROMPTING IMPLEMENTATION RESULT:")
print(classify(
    "Reset my password",
    labels=["account issue", "general inquiry"]
))
print("\n")
print(f"DSPY IMPLEMENTATION RESULT:")
print(classify_dspy(
    "Reset my password",
    labels=["account issue", "general inquiry"]
))


print(classify(
    "The app crashes when I try to upload a file.",
    labels=["bug", "feature request", "inquiry"]
))

print(classify(
    "I like to stay inside.",
    labels=["cat person", "dog person"]
))

class Product(pydantic.BaseModel):
    feature: str

print(f"MANUAL PROMPTING IMPLEMENTATION RESULT:")
print(extract(
    "I love my new phone's camera, but it could have better battery life.",
    model=Product.model_json_schema(),
    instructions="Product features"
))

print(f"DSPY IMPLEMENTATION RESULT:")
print(extract_dspy(
    "I love my new phone's camera, but it could have better battery life.",
    model=json.dumps(Product.model_json_schema()),
    instructions="Product features"
))

class Location(pydantic.BaseModel):
    city: str
    country: str

print(extract(
    "I moved from BOS to Sarajevo to Paris to Taipei",
    model=Location.model_json_schema(),
    instructions="Cities in Asia"
))

class Money(pydantic.BaseModel):
    amount: float

print(extract(
    "I paid $10 for 3 tacos and got a dollar and 25 cents back.",
    model=Money.model_json_schema(),
    instructions="Only extract money"
))

class Cat(pydantic.BaseModel):
    name: str

print(generate(
    n = 6,
    instruction="names for cats inspired by Chance the Rapper",
    model=Cat.model_json_schema()
))

class Party(pydantic.BaseModel):
    theme: str

print(generate(
    n = 5,
    instruction="theme ideas for a winter birthday party",
    model=Party.model_json_schema()
))

print(define(
    "contract"
))

print(define(
    "novel"
))

# TODO: Validate output to only include response
print(f"MANUAL PROMPTING IMPLEMENTATION RESULT:")
print(
    spellCheck("me and my frend had a rilly nice wok in the park 2day")
)

print("DSPY IMPLEMENTATION RESULT:")
print(
    spellCheck_dspy("me and my frend had a rilly nice wok in the park 2day")
)