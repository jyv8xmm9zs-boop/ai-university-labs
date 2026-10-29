import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

# Saved on your computer so the tutor still knows you after quit.
memory_file = Path("chat_memory.json")

# The system prompt: the AI's job and personality
def fresh_messages():
    return [
        {"role": "system", "content": "You are a friendly AI tutor. Explain things simply, like I'm a beginner, with one short example."}
    ]


messages = fresh_messages()

if memory_file.exists():
    messages = json.loads(memory_file.read_text(encoding="utf-8"))


def save_memory():
    memory_file.write_text(json.dumps(messages, indent=2), encoding="utf-8")


print("Chat with your tutor! Type 'quit' to stop, or 'forget' to erase memory.\n")

while True:                                   # keep chatting until you quit
    question = input("You: ")
    if question.lower() == "quit":
        break
    if question.lower() == "forget":
        messages = fresh_messages()
        save_memory()
        print("\nTutor: Memory erased. We can start fresh.\n")
        continue
    messages.append({"role": "user", "content": question})        # save your message
    response = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    answer = response.choices[0].message.content
    messages.append({"role": "assistant", "content": answer})     # save the AI's reply
    save_memory()
    print("\nTutor:", answer, "\n")
