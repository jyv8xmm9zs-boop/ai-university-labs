import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
client = OpenAI()
# ---------- Notes search (RAG from Session 6) ----------
def embed(texts):
    r = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return [d.embedding for d in r.data]
def load_notes():
    try:
        return [l.strip() for l in open("my_notes.txt") if l.strip()]
    except FileNotFoundError:
        return []
def search_notes(query):
    notes = load_notes()
    if not notes:
        return "No notes yet."
    vecs = embed(notes)
    q = embed([query])[0]
    ranked = sorted(zip(notes, vecs), key=lambda n: sum(a*b for a, b in zip(q, n[1])), reverse=True)
    return "\n".join(n[0] for n in ranked[:3])
# ---------- Other tools ----------
def get_time():
    return datetime.now().strftime("%A %B %d, %Y, %I:%M %p")
def calculator(expression):
    try:
        return str(eval(expression, {"__builtins__": {}}))
    except Exception as e:
        return f"Error: {e}"
def add_note(text):
    with open("my_notes.txt", "a") as f:
        f.write(text + "\n")
    return "Note saved."
TOOLS = {"search_notes": search_notes, "get_time": get_time, "calculator": calculator, "add_note": add_note}
def tool(name, desc, props=None, required=None):
    return {"type": "function", "function": {"name": name, "description": desc,
            "parameters": {"type": "object", "properties": props or {}, "required": required or []}}}
tools = [
    tool("search_notes", "Search the user's personal notes for facts about them", {"query": {"type": "string"}}, ["query"]),
    tool("get_time", "Get the current date and time"),
    tool("calculator", "Do math, e.g. '25*4+10'", {"expression": {"type": "string"}}, ["expression"]),
    tool("add_note", "Save a new fact the user wants remembered", {"text": {"type": "string"}}, ["text"]),
]
# ---------- Personality + memory ----------
messages = [{"role": "system", "content":
    "You are Sky's personal AI assistant. Be friendly and concise. "
    "Search notes before answering questions about Sky. "
    "If Sky says 'remember...', save it with add_note. Use tools whenever helpful."}]
print("Your assistant is ready. Type 'quit' to stop.\n")
# ---------- Chat loop + agent loop ----------
while True:
    user = input("You: ")
    if user.lower() == "quit":
        break
    messages.append({"role": "user", "content": user})
    for step in range(5):
        r = client.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)
        msg = r.choices[0].message
        messages.append(msg)
        if not msg.tool_calls:
            print("\nAssistant:", msg.content, "\n")
            break
        for call in msg.tool_calls:
            args = json.loads(call.function.arguments or "{}")
            print(f"  [using {call.function.name} {args}]")
            result = TOOLS[call.function.name](**args)
            messages.append({"role": "tool", "tool_call_id": call.id, "content": result})
