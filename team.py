from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
client = OpenAI()
def agent(role, task):
    """One agent = one system prompt (its job) + a task."""
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": role},
                  {"role": "user", "content": task}],
    )
    return r.choices[0].message.content
RESEARCHER = "You are a researcher. List the 5 most important, accurate facts about the topic as short bullets."
WRITER = "You are a writer. Turn research notes into a clear, engaging 150-word post for beginners."
EDITOR = "You are a strict editor. Give 3 specific improvements for this post. Be brief."
topic = input("Topic: ")
print("\n--- Researcher working ---")
facts = agent(RESEARCHER, topic)
print(facts)
print("\n--- Writer drafting ---")
draft = agent(WRITER, f"Topic: {topic}\nResearch:\n{facts}")
print(draft)
print("\n--- Editor reviewing ---")
feedback = agent(EDITOR, draft)
print(feedback)
print("\n--- Writer revising ---")
final = agent(WRITER, f"Rewrite this post using the feedback.\nPost:\n{draft}\nFeedback:\n{feedback}")
print(final)
with open("post.md", "w") as f:
    f.write(final)
print("\nSaved to post.md")
