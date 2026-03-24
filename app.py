from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__, static_folder="static")
CORS(app)

HF_TOKEN = os.environ.get("HF_TOKEN", "")

SYSTEM_PROMPT = """You are MicroFrog, a highly intelligent, multi-talented AI assistant. You are professional yet warm, concise yet thorough. You can help with writing, coding, analysis, brainstorming, translation, math, and any topic. Always respond helpfully and confidently. Keep responses clear and well-structured."""

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    messages = data.get("messages", [])

    if not messages:
        return jsonify({"error": "No messages provided"}), 400

    full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages

    try:
        client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=HF_TOKEN,
        )

        completion = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3-70B-Instruct",
            messages=full_messages,
            max_tokens=600,
            temperature=0.7,
        )

        reply = completion.choices[0].message.content.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health")
def health():
    return jsonify({"status": "ok", "model": "Llama-3-70B", "name": "MicroFrog"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
