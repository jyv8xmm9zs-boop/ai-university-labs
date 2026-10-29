import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()          # reads your key from the .env file
client = OpenAI()      # connects to OpenAI using that key

# Saved on your computer so the chat is still here after quit.
memory_file = Path("memory.json")

# Personality: this system message tells the model who to be.
# Memory: this list keeps every turn and is sent again each time.
messages = [
    {
        "role": "system",
        "content": (
            "You are a friendly tutor at AI University. "
            "Speak in short, clear sentences. "
            "Remember what the student already told you."
        ),
    }
]

if memory_file.exists():
    messages = json.loads(memory_file.read_text(encoding="utf-8"))


def save_memory():
    memory_file.write_text(json.dumps(messages, indent=2), encoding="utf-8")


print("Talk to your AI. Type quit to stop.")
while True:
    question = input("Ask the AI: ")
    if question.strip().lower() in {"quit", "exit"}:
        break

    messages.append({"role": "user", "content": question})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )
    answer = response.choices[0].message.content
    messages.append({"role": "assistant", "content": answer})
    save_memory()
    print("\nAI:", answer, "\n")
