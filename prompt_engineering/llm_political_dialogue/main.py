from openai import OpenAI

client = OpenAI()


def fetch_response(messages):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    return completion.choices[0].message.content

def generate_dialogue():
    messages = []

    for file_name in ["system_prompt.txt", "costar_prompt.txt", "few_shot_prompt.txt", "chain_of_thought_prompt.txt"]:
        with open(file_name, 'r') as file:
            content = file.read()

        messages.append({
            "role": "system" if file_name == "system_prompt.txt" else "user",
            "content": content
        })


    with open('dialogue.txt', 'w') as file:
        file.write(fetch_response(messages))
    

if __name__ == "__main__":
    generate_dialogue()