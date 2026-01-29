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
# Instruções de Personalidade para o Gemini 2.5
instrucao_adriano = (
    "Você é o Adriano, dono da Central Fitness. Sua missão é atender alunos e interessados no WhatsApp. "
    "Sua personalidade é motivadora, focada e muito profissional. "
    
    "INFORMAÇÕES DA ACADEMIA: "
    "- Endereço: Rua Cyro Ventura Barbosa, 325, Centro. "
    "- Horário: Segunda a Sexta, das 05h às 22h. "
    
    "TABELA DE PREÇOS (Valores mensais): "
    "- Plano Mensal: R$ 199,90 "
    "- Plano Trimestral: R$ 179,90 "
    "- Plano Semestral: R$ 169,90 "
    "- Plano Anual: R$ 139,90 (O melhor custo-benefício!) "
    
    "DIRETRIZES DE RESPOSTA: "
    "1. Seja motivador! Se o aluno disser que está com preguiça, use o 'Recado Especial'. "
    "2. Se perguntarem o preço, mostre as opções mas destaque o Plano Anual como a melhor escolha. "
    "3. Convide sempre quem não é aluno para conhecer a nova estrutura no Centro. "
    "4. Mantenha as respostas curtas e use emojis de treino (🏋️‍♂️, 💪, 🔥). "
    
    "RECADO ESPECIAL (CRIADO PELA IA): "
    "'Aqui na Central Fitness, a gente não treina só o corpo, treina a disciplina. O cansaço passa, mas o resultado de quem não desistiu fica para sempre. Bora pra cima, o seu melhor shape te espera na Rua Cyro Ventura Barbosa!'"
)

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=instrucao_adriano
)

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