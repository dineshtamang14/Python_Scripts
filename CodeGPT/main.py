import openai


openai.api_key = ""
model_engine = "text-davinci-002"
prompt = str(input("Enter your Question: "))

completion = openai.Completion.create(
        engine = model_engine,
        prompt=prompt,
        max_tokens = 1024,
        n = 1,
        stop = None,
        temperature = 0.9,
        )

response = completion.choices[0].text
print(response)
