from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

# The system prompt: the AI's job and personality
messages = [
    {"role": "system", "content": "You are a friendly AI tutor. Explain things simply, like I'm a beginner, with one short example."}
]

print("Chat with your tutor! Type 'quit' to stop.\n")

while True:                                   # keep chatting until you quit
    question = input("You: ")
    if question.lower() == "quit":
        break
    messages.append({"role": "user", "content": question})        # save your message
    response = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    answer = response.choices[0].message.content
    messages.append({"role": "assistant", "content": answer})     # save the AI's reply
    print("\nTutor:", answer, "\n")
