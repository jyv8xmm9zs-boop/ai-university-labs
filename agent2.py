import json
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

# --- Tools ---
def get_time():
    return datetime.now().strftime("%A %B %d, %Y, %I:%M %p")

def calculator(expression):
    try:
        return str(eval(expression, {"__builtins__": {}}))   # simple math only
    except Exception as e:
        return f"Error: {e}"

def save_note(text):
    with open("notes.txt", "a") as f:
        f.write(text + "\n")
    return "Saved."

TOOLS = {"get_time": get_time, "calculator": calculator, "save_note": save_note}

tools = [
    {"type": "function", "function": {"name": "get_time", "description": "Get current date and time",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "calculator", "description": "Do math, e.g. '25*4+10'",
        "parameters": {"type": "object", "properties": {"expression": {"type": "string"}}, "required": ["expression"]}}},
    {"type": "function", "function": {"name": "save_note", "description": "Save a note to notes.txt",
        "parameters": {"type": "object", "properties": {"text": {"type": "string"}}, "required": ["text"]}}},
]

messages = [{"role": "system", "content": "You are a helpful agent. Use tools step by step until the task is done."}]
messages.append({"role": "user", "content": input("You: ")})

# --- The agent loop ---
for step in range(5):                      # safety limit: max 5 steps
    response = client.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)
    msg = response.choices[0].message
    messages.append(msg)
    if not msg.tool_calls:                 # no more tools needed, so we're done
        print("\nAI:", msg.content)
        break
    for call in msg.tool_calls:
        name = call.function.name
        args = json.loads(call.function.arguments or "{}")
        print(f"[Step {step+1}] using {name} {args}")
        result = TOOLS[name](**args)
        messages.append({"role": "tool", "tool_call_id": call.id, "content": result})
