from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import openai
import os
from pathlib import Path
# load contents of sampleSimplified.json as text
txt = Path('sampleSimplified.json').read_text()



load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


llm = OpenAI()
chat_model = ChatOpenAI()


# user_input = "Find me the piston and the crankshaft."
user_input = "Which parts are the plastic cover on the very top of the engine?"



prompt = """
I have the following JSON file describing a 3D model:
{txt}
The user asks you the following question: 
###
"{user_input}"
###. 
Your answer should only be a list of strings that looks like this: ["part1", "part2", "part3"] and nothing else. If the answer is too long then make sure to only return the 30 most important parts and make sure to close the list.
""".format(txt=txt, user_input=user_input)

print(prompt)


answer = llm.predict(prompt)
print(answer)

