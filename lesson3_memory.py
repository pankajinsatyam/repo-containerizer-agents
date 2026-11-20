from openai import OpenAI

client = OpenAI()
MODEL = "gpt-5.4-nano"

def ask(messages):
    r = client.chat.completions.create(model=MODEL, messages=messages)
    return r.choices[0].message.content, r.usage.prompt_tokens

# ---------- Part A: two separate calls ----------
answer, _ = ask([{"role": "user", "content": "My app is a Java 17 Spring Boot service on port 8080. Just reply OK."}])
print("Call 1:", answer)

answer, _ = ask([{"role": "user", "content": "Which port does my app use?"}])
print("Call 2:", answer)      # it won't know!

# ---------- Part B: a chat that remembers ----------
print("\n--- Chat mode (type 'exit' to stop) ---")
history = [{"role": "system", "content": "You are a helpful DevOps engineer. Answer briefly."}]

while True:
    question = input("You: ")
    if question == "exit":
        break
    history.append({"role": "user", "content": question})        # add my question
    answer, tokens = ask(history)                                 # send EVERYTHING
    history.append({"role": "assistant", "content": answer})     # add its reply
    print("AI:", answer)
    print(f"   (tokens sent this time: {tokens})")
