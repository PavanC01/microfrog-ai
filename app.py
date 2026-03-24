from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder="static")
CORS(app)

HF_TOKEN = os.environ.get("HF_TOKEN", "")
HF_API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-70B-Instruct"

SYSTEM_PROMPT = """You are MicroFrog, a highly intelligent, multi-talented AI assistant. You are professional yet warm, concise yet thorough. You can help with writing, coding, analysis, brainstorming, translation, math, and any topic. Always respond helpfully and confidently. Keep responses clear and well-structured."""

def build_prompt(messages):
    prompt = "<|begin_of_text|>"
    prompt += f"<|start_header_id|>system<|end_header_id|>\n\n{SYSTEM_PROMPT}<|eot_id|>"
    for msg in messages:
        role = msg.get("role")
        content = msg.get("content", "")
        prompt += f"<|start_header_id|>{role}<|end_header_id|>\n\n{content}<|eot_id|>"
    prompt += "<|start_header_id|>assistant<|end_header_id|>\n\n"
    return prompt

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    messages = data.get("messages", [])

    if not messages:
        return jsonify({"error": "No messages provided"}), 400

    prompt = build_prompt(messages)

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 600,
            "temperature": 0.7,
            "top_p": 0.9,
            "do_sample": True,
            "return_full_text": False
        }
    }

    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=60)
        result = response.json()

        if isinstance(result, list) and result[0].get("generated_text"):
            reply = result[0]["generated_text"].strip()
            # Clean up any trailing tokens
            import re
            reply = re.sub(r"<\|.*?\|>", "", reply).strip()
            return jsonify({"reply": reply})
        elif isinstance(result, dict) and result.get("error"):
            return jsonify({"error": result["error"]}), 500
        else:
            return jsonify({"error": "Unexpected response from model"}), 500

    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timed out. The model may be loading, please try again."}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health")
def health():
    return jsonify({"status": "ok", "model": "Llama-3-70B", "name": "MicroFrog"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
