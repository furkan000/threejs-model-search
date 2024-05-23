import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
# chat_model = ChatOpenAI()


from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    # {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Give me a random number"},
    {"role": "assistant", "content": "17"},
    {"role": "user", "content": "increment by 1"},
  ]
)

print(completion.choices[0].message)