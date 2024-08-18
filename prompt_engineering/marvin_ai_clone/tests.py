import pydantic
from marvin_ai_clone import classify, extract, generate, define, spellCheck
# Test cases:
print(classify(
    "The app crashes when I try to upload a file.",
    labels=["bug", "feature request", "inquiry"]
))

class Location(pydantic.BaseModel):
    city: str
    country: str


print(extract(
    "I moved from BOS to Sarajevo",
    model=Location.model_json_schema(),
))

class Cat(pydantic.BaseModel):
    name: str

print(generate(
    n = 4,
    instruction="names for cats inspired by Chance the Rapper",
    model=Cat.model_json_schema()
))

print(define(
    "contract"
))

print(
    spellCheck("me and my frend had a rilly nice wok in the park 2day")
)