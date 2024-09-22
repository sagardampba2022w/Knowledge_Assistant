# prompt_builder.py

def build_prompt(question, search_results):
    prompt_template = """
You're a syndicated market research provider. Answer the QUESTION based on the CONTEXT from the FAQ database.
Use only the facts from the CONTEXT when answering the QUESTION.

QUESTION: {question}

CONTEXT: 
{context}
""".strip()

    context = ""
    for doc in search_results:
        context += f"Category: {doc['Category']}\nQuestion: {doc['Question']}\nAnswer: {doc['Answer']}\n\n"

    prompt = prompt_template.format(question=question, context=context)
    return prompt
