from llm import ask_llm


response = ask_llm(
    system_prompt="You are a helpful AI engineering assistant.",
    user_prompt="Explain what an HTTP 500 error means in one sentence.",
)

print(response)