from mcp.server.fastmcp import FastMCP
mcp = FastMCP("my-notes")
NOTES_FILE = r"C:\Users\skyse\ai-university-labs\my_notes.txt"   # fix this path if your folder is elsewhere
@mcp.tool()
def read_notes() -> str:
    """Read all of Sky's personal notes."""
    try:
        return open(NOTES_FILE).read() or "No notes yet."
    except FileNotFoundError:
        return "No notes yet."
@mcp.tool()
def add_note(text: str) -> str:
    """Save a new note for Sky."""
    with open(NOTES_FILE, "a") as f:
        f.write(text + "\n")
    return "Saved."
if __name__ == "__main__":
    mcp.run()
