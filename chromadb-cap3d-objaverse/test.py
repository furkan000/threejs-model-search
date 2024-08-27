import openai
from openai import OpenAI

client = OpenAI(api_key="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")

def text_embedding(text) -> None:
    return client.embeddings.create(input = [text], model="text-embedding-3-small").data[0].embedding


print(len(text_embedding("Hello, World!")))