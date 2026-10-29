import json
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

# 1. The tool: a normal Python function
def get_time():
    return datetime.now().strftime("%A %B %d, %Y, %I:%M %p")

# 2. Describe the tool so the AI knows it exists
tools = [{
    "type": "function",
    "function": {
        "name": "get_time",
        "description": "Get the current date and time",
        "parameters": {"type": "object", "properties": {}},
    },
}]

messages = [{"role": "system", "content": "You are a helpful assistant. Use tools when needed."}]

print("Ask your agent. Type 'quit' to stop.\n")

while True:
    question = input("You: ")
    if question.lower() == "quit":
        break
    messages.append({"role": "user", "content": question})

    # 3. Ask the AI. It may answer directly or ask to use the tool
    response = client.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)
    msg = response.choices[0].message

    if msg.tool_calls:                       # the AI wants to use a tool
        print("[AI decided to use the tool: get_time]")
        messages.append(msg)
        for call in msg.tool_calls:
            result = get_time()              # your code runs the tool
            messages.append({"role": "tool", "tool_call_id": call.id, "content": result})
        # 4. Send the tool result back so the AI can finish its answer
        final = client.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)
        answer = final.choices[0].message.content
        messages.append({"role": "assistant", "content": answer})
        print("AI:", answer, "\n")
    else:
        messages.append(msg)
        print("AI:", msg.content, "\n")
