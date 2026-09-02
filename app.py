from flask import Flask, render_template, request
from datetime import datetime
import resend 
import json
from dotenv import load_dotenv
import os

load_dotenv()

resend.api_key = os.getenv("API_KEY")
with open('dados.json', 'r', encoding="utf-8") as f:
    dados = json.load(f)

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        nome = request.form['name'] 
        email = request.form['email']
        mensagem = request.form['message']

        dados_mensagem = {
            'nome' : nome,
            'email' : email,
            'mensagem' : mensagem,
            'data' : f'{datetime.today ()}'
        }

        dados.append(dados_mensagem)
        with open('dados.json', 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent= 4, ensure_ascii=False)

        params: resend.Emails.SendParams = {
        "from": "DoPet <onboarding@resend.dev>",
        "to": ["ya147474@gmail.com"],
        "subject": f"Solicitação de adoção de {nome}",
        "html": f"Email: {email}<br>{mensagem}"
        }

        email_resend = resend.Emails.send(params)

        return render_template("index.html")
        
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
    