import json, os
from openai import OpenAI

client = OpenAI()
MODEL = "gpt-5.4-nano"

# ---------- 1. The real Python functions (the "hands") ----------
def list_files(folder):
    return "\n".join(os.listdir(folder))

def read_file(path):
    with open(path) as f:
        return f.read()

# ---------- 2. Describe the tools to the LLM (like a menu) ----------
tools = [
    {"type": "function", "function": {
        "name": "list_files",
        "description": "List the files inside a folder.",
        "parameters": {
            "type": "object",
            "properties": {"folder": {"type": "string", "description": "Folder path, e.g. sample_app"}},
            "required": ["folder"]}}},
    {"type": "function", "function": {
        "name": "read_file",
        "description": "Read and return the text of a file.",
        "parameters": {
            "type": "object",
            "properties": {"path": {"type": "string", "description": "File path, e.g. app.py"}},
            "required": ["path"]}}},
]

messages = [
    {"role": "system", "content": "You are a DevOps engineer. Use the tools to look at files. Never guess file contents."},
    {"role": "user",   "content": "Read sample_app/requirements.txt and tell me which packages the app needs."},
]

# ---------- 3. First call: the LLM decides if it needs a tool ----------
response = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
msg = response.choices[0].message

if not msg.tool_calls:
    print("No tool needed. Answer:", msg.content)
    raise SystemExit

print("The LLM is asking us to run a tool:")
messages.append(msg)                      # remember its request in the history

for call in msg.tool_calls:
    name = call.function.name
    args = json.loads(call.function.arguments)     # the LLM sends arguments as JSON text
    print(f"   -> {name}({args})")

    # ---------- 4. OUR code runs the tool ----------
    try:
        if name == "list_files":
            result = list_files(**args)
        elif name == "read_file":
            result = read_file(**args)
        else:
            result = f"Unknown tool: {name}"
    except Exception as e:
        result = f"ERROR: {e}"            # tell the LLM what went wrong instead of crashing

    print("   <- result:", result[:200])
    messages.append({"role": "tool", "tool_call_id": call.id, "content": result})

# ---------- 5. Second call: the LLM uses the result to answer ----------
response = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
final = response.choices[0].message

if final.tool_calls:
    print("\nIt wants ANOTHER tool:", [c.function.name for c in final.tool_calls])
    print("(Handling this automatically is Lesson 4!)")
else:
    print("\nFinal answer:\n", final.content)
