from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="gemma4",
    temperature=0.7
)


def ask_llm(question):
    prompt = f"""
You are an AI interview coach.
Answer interview questions clearly in short bullet points.

Question: {question}
"""

    response = llm.invoke(prompt)

    return response.content