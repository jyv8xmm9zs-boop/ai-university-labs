from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
client = OpenAI()
# 1. Load notes (one note per line)
notes = [line.strip() for line in open("my_notes.txt") if line.strip()]
# 2. Turn every note into an embedding (a list of numbers that captures meaning)
def embed(texts):
    result = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return [item.embedding for item in result.data]
note_vectors = embed(notes)
# 3. Similarity: how close two meanings are (higher = more similar)
def similarity(a, b):
    return sum(x * y for x, y in zip(a, b))
question = input("Ask about your notes: ")
q_vector = embed([question])[0]
# 4. Find the 2 most relevant notes
scored = sorted(zip(notes, note_vectors), key=lambda n: similarity(q_vector, n[1]), reverse=True)
top_notes = [n[0] for n in scored[:2]]
print("\n[Found these notes:]", top_notes)
# 5. Give the AI only those notes and ask it to answer
prompt = f"Answer using ONLY these notes:\n{top_notes}\n\nQuestion: {question}"
response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
print("\nAI:", response.choices[0].message.content)
