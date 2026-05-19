from groq import Groq
from dotenv import load_dotenv
import os
import json

# Carrega o .env
load_dotenv()

# Configura o cliente
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("Chat iniciado! Digite 'sair' para encerrar.\n")

memoria = []

#Carrega o historico de mensagens 

try:
    with open("historico.json", "r") as f:
     memoria = json.load(f)
except:
    memoria = []


memoria.append({
    "role": "system",
    "content": "Voce tera a personalidade da personagem Plim de Smiling Friends ele trabalha em uma empresa que faz as pessoas sorrirem, quem ta triste liga para a empresa e  Pim Pimling e o Charlie vao tentar resolver o Plim é  Otimista, baixinho e rosa, é o funcionário idealista do grupo. Ele tenta sempre fazer o bem, mesmo que acabe se envolvendo em situações caóticas."
    })

# Loop do chat
while True:
    user_input = input("Você: ")
    
    
    memoria.append({"role": "user", "content": user_input})

    messages = memoria
    
    if user_input.lower() == "sair":
        print("Encerrando chat. Até logo!")
        break
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages = memoria
    )

    memoria.append({"role": "assistant", "content": response.choices[0].message.content})

    with open("historico.json", "w") as f:
        json.dump(memoria, f)

    print(f"IA: {response.choices[0].message.content}\n")