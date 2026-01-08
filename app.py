import os
import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# OpenRouter Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("ERROR: OPENROUTER_API_KEY is not set in environment variables.")

# Free model available
MODEL_ID = "deepseek/deepseek-r1:free"

@app.route('/')
def home():
    return render_template_string('''
        <h1>OpenRouter Chatbot</h1>
        <input type="text" id="userInput" placeholder="Type here...">
        <button onclick="sendMessage()">Send</button>
        <p id="response"></p>
        <script>
            async function sendMessage() {
                const input = document.getElementById('userInput').value;
                const res = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: input})
                });
                const data = await res.json();
                document.getElementById('response').innerText = data.reply;
            }
        </script>
    ''')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "yourapp.example",
        "X-Title": "My Chatbot App"
    }
    
    payload = {
        "model": MODEL_ID,
        "messages": [{"role": "user", "content": user_message}]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload
    )
    
    if response.status_code == 200:
        reply = response.json()['choices'][0]['message']['content']
        return jsonify({"reply": reply})
    else:
        return jsonify({"reply": "Error: " + response.text}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
