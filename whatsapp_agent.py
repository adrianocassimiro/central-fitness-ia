import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega as chaves do arquivo .env [cite: 78, 79]
load_dotenv()

# Configuração do Gemini 2.5 Flash
# Certifique-se de que sua API_KEY tenha permissão para o modelo 2.5
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Definindo o modelo específico Gemini 2.5 Flash
model = genai.GenerativeModel('gemini-2.5-flash') 

app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def webhook():
    # 1. Recebe a mensagem e o número de quem enviou [cite: 91, 94]
    msg_cliente = request.values.get('Body', '')
    num_cliente = request.values.get('From', '')
    
    print(f"Mensagem recebida de {num_cliente}: {msg_cliente}")

    try:
        # 2. IA gera a resposta com personalidade (SYSTEM_PROMPT) [cite: 145]
        # Aqui definimos a personalidade do Adriano da Central Fitness [cite: 9, 148]
        prompt_sistema = (
            "Você é o Adriano, dono da Central Fitness. "
            "Sua personalidade é motivadora, educada e focada em resultados. "
            "Responda de forma curta (máximo 3 linhas) e use emojis de treino. "
            f"O cliente disse: {msg_cliente}"
        )
        
        response = model.generate_content(prompt_sistema)
        resposta_ia = response.text

        # 3. Twilio prepara a resposta para o WhatsApp [cite: 74, 92]
        resp = MessagingResponse()
        resp.message(resposta_ia)
        
        print(f"IA respondeu: {resposta_ia}")
        return str(resp)

    except Exception as e:
        print(f"Erro ao processar: {e}")
        resp = MessagingResponse()
        resp.message("Opa, aqui é o Adriano. Tive um pequeno problema técnico, mas já te respondo!")
        return str(resp)

if __name__ == "__main__":
    # Mudamos para 0.0.0.0 para o Render conseguir enxergar o robô
    app.run(host='0.0.0.0', port=5000)