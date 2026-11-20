from openai import OpenAI

client = OpenAI()          # picks up OPENAI_API_KEY automatically
MODEL = "gpt-5.4-nano"     # change this one line to try other models

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a senior DevOps engineer. Answer briefly and simply."},
        {"role": "user",   "content": "What is a multi-stage Dockerfile? Answer in 3 lines."},
    ],
)

print(response.choices[0].message.content)
print("---")
print("Tokens sent:    ", response.usage.prompt_tokens)
print("Tokens received:", response.usage.completion_tokens)
