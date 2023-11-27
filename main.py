from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import openai
import os
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS

# load contents of sampleSimplified.json as text
txt = Path('sampleSimplified.json').read_text()



load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


llm = OpenAI()
chat_model = ChatOpenAI()


# user_input = "Find me the piston and the crankshaft."
# user_input = "Which parts are the plastic cover on the very top of the engine?"

available_functions = """
highlight objectNames
hide objectNames
recolor objectNames color
resize objectNames x y z
rotate objectNames x y z
move objectNames x y z
playAnimation objectNames
"""

prompt_placeholder = """
I have the following JSON file describing a 3D model of a motor which has 8 pistons.
{txt}
The user asks you the following question: 
###
"{user_input}"
###.
You have the following functions available:
{available_functions}
You can execute multiple function calls but make sure to put each call on a seperate lines. 
Animating and highlighting are great to show a user where a part is located. Dont rotate, hide, recolor without a reason.
Call functions like these following examples, make sure to only use whitespace when separating parameters. Do not use whitespace between list items. 
recolor ['name1','name2'] 0x00ff00
resize ['name1','name2'] 1.5 -1.5 0.5
Only answer in function calls, do not add any other text.
"""

# Your answer should only be a list of strings that looks like this: ["part1","part2", "part3"] and nothing else. If the answer is too long then make sure to only return the 30 most important parts and make sure to close the list.



# print(prompt)



# -------------------------------------------------------


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/', methods=['POST'])
def handlePost():
    text_data = request.data.decode('utf-8')
    print("user: " + text_data)
    response = promptLLM(text_data)
    return response


def promptLLM(user_query):
    prompt = prompt_placeholder.format(txt=txt, user_input=user_query, available_functions=available_functions)
    # print("prompt:\n" + prompt)
    answer = llm.predict(prompt)
    # answer = """highlight ['cylinderHeadBoltRight001', 'cylinderHeadBoltRight002', 'cylinderHeadBoltRight003','cylinderHeadBoltRight004','cylinderHeadBoltLeft001','cylinderHeadBoltLeft002','cylinderHeadBoltLeft003','cylinderHeadBoltLeft004'] 
# recolor ['cylinderHeadBoltRight001', 'cylinderHeadBoltRight002', 'cylinderHeadBoltRight003','cylinderHeadBoltRight004','cylinderHeadBoltLeft001','cylinderHeadBoltLeft002','cylinderHeadBoltLeft003','cylinderHeadBoltLeft004'] 0x0000FF
# """
    print("answer: " + answer)
    return answer
    # return "test"


# user_query = "highlight and recolor head gasket"
# print(llm.predict( prompt_placeholder.format(txt=txt, user_input=user_query, available_functions=available_functions)))



if __name__ == '__main__':
    app.run(debug=True, port=5000)





# answer = llm.predict(prompt)
# print(answer)