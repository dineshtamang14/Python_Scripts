import openai
import os



def get_response(model_engine, prompt):
    '''Takes prompt as a input and returns a responses'''
    completion = openai.Completion.create(
        engine = model_engine,
        prompt=prompt,
        max_tokens = 1024,
        n = 1,
        stop = None,
        temperature = 0.9,
    )
    
    return completion.choices[0].text

        
value = os.getenv("apiKey", default=None)
openai.api_key = value
model_engine = "text-davinci-002"
prompt = str(input("Enter your Question: "))


response = get_response(model_engine, prompt)
print(response)