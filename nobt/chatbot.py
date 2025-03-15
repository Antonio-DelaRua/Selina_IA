import openai
from config import get_api_key
import json

OPENAI_API_KEY = get_api_key()
openai.api_key = OPENAI_API_KEY

def chat_with_bot(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,
            temperature=0.7,
        )
        response_text = response.choices[0].message['content'].strip()
        save_to_history(prompt, response_text)
        save_jsnon_to_history(prompt, response_text)
        return response_text
    except openai.OpenAIError as e:
        print(f"Error al llamar a la API de OpenAI: {e}")
        return "Lo siento, ocurrió un error al intentar comunicarme con el chatbot."

def save_to_history(prompt, response):
    with open("chat_history.txt", "a", encoding="utf-8") as file:
        file.write(f"Usuario: {prompt}\nChatbot: {response}\n\n")

def save_jsnon_to_history(prompt, response):
    with open("historic.json", "r+", encoding="utf-8") as file:
        jsonObject =  json.loads(file.read())
        
        arrayConversaciones  = jsonObject["converascion"]
        jsonObject["usuarios"] = "ejemplo user"
        item = {'question': prompt, 'response': response}
        arrayConversaciones.append(item)
        file.seek(0)
        file.truncate()
        file.write(str(json.dumps(jsonObject)).encode().decode('unicode_escape'))

if __name__ == "__main__":
    prompt = input("Escribe tu mensaje para el chatbot: ")
    respuesta = chat_with_bot(prompt)
    print(f"Chatbot: {respuesta}")