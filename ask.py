from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()          # reads your key from the .env file
client = OpenAI()      # connects to OpenAI using that key

question = input("Ask the AI: ")
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": question}],
)
print("\nAI:", response.choices[0].message.content)
