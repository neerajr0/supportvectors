import pydantic
from marvin_ai_clone import classify, extract, generate, define, spellCheck
# Test cases:

print(classify(
    "I like to stay inside.",
    labels=["dog person", "cat person"]
))

print(classify(
    "The app crashes when I try to upload a file.",
    labels=["bug", "feature request", "inquiry"]
))

class Location(pydantic.BaseModel):
    city: str
    country: str


print(extract(
    "I moved from BOS to Sarajevo to Paris to Taipei",
    model=Location.model_json_schema(),
    instructions="Cities in Europe"
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
    n = 4,
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

print(
    spellCheck("me and my frend had a rilly nice wok in the park 2day")
)