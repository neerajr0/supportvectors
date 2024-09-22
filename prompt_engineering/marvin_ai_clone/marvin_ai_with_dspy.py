# See https://github.com/prefecthq/marvin
from pydantic import BaseModel, Field
from typing import List, Type, Dict
import dspy

model = dspy.OpenAI(model='gpt-4o-mini', max_tokens=500)
dspy.settings.configure(lm=model)

class ClassifyText(dspy.Signature):
    """Classifies given a text and list of labels."""

    text = dspy.InputField(desc="a statement that may or may not have some category associated with it.")
    labels = dspy.InputField(desc="a list of labels that represent the valid options to choose from.")
    category = dspy.OutputField()

def classify_dspy(text, labels):
    """
    Classifies given a text and list of labels
    """
    classifier = dspy.ChainOfThought(ClassifyText)
    return classifier(text=text, labels="\n".join(labels))


# TODO: Figure out custom types for input/output: https://dspy-docs.vercel.app/docs/building-blocks/typed_predictors
class Input(BaseModel):
    text: str = Field(description="a statement that may or may not contain instances of a certain category to extract.")
    model: str = Field(description="A Pydantic model in dict form that you should look to extract instances of in the provided text.")
    instructions: str = Field(description="If provided, only return those instances in text that match the conditions of the instruction.")

class Output(BaseModel):
    matches: List[str] = Field(description="A list of instances of the Pydantic model provided in the input category found in the input text.")

class QASignature(dspy.Signature):
    """Answer the question based on the context and query provided, and on the scale of 10 tell how confident you are about the answer."""

    input: Input = dspy.InputField()
    output: Output = dspy.OutputField()


def extract_dspy(text, model, instructions=""):
    """
    Extracts given text and a target pydantic model
    """
    cot_predictor = dspy.TypedChainOfThought(QASignature)

    input_instance = Input(
        text=text,
        model=model,
        instructions=instructions
    )

    prediction = cot_predictor(input=input_instance)
    return prediction
    

class SpellCheck(dspy.Signature):
    """Classifies given a text and list of labels."""

    text = dspy.InputField(desc="A piece of text requiring spelling and grammatical fixes.")
    category = dspy.OutputField(desc="The corrected text with no spelling or grammatical errors.")

def spellCheck_dspy(text):
    """
    Fixes spelling and grammar errors in a text
    """
    spell_checker = dspy.ChainOfThoughtWithHint(SpellCheck)

    return spell_checker(text=text, hint="Look out for grammatical errors, not just spelling.")
