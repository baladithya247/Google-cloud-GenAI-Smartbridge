import google.generativeai as genai

genai.configure(api_key="AIzaSyBUSyS2AOlh8rXADFjfAkeVJ5B_uYh7lxA")

models = genai.list_models()

for m in models:
    print(m.name)
