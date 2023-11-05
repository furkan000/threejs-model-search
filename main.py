from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI


llm = OpenAI()
chat_model = ChatOpenAI()

answer = chat_model.predict("Hello, how are you?")
print(answer)

