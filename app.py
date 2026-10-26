
import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "app": "Jarvis VR 1",
        "status": "running"
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/chat", methods=["POST"])
def chat():
    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        return jsonify({
            "error": "OPENAI_API_KEY is not configured"
        }), 503

    data = request.get_json(silent=True) or {}
    message = data.get("message", "")

    if not isinstance(message, str) or not message.strip():
        return jsonify({"error": "Message is required"}), 400

    if len(message) > 10000:
        return jsonify({"error": "Message is too long"}), 400

    try:
        client = OpenAI(api_key=api_key)

        response = client.responses.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"),
            instructions=(
                "You are Jarvis, a helpful AI assistant. "
                "Reply in Gujarati, Hindi, or English "
                "according to the user's language."
            ),
            input=message
        )

        return jsonify({"reply": response.output_text})

    except Exception:
        app.logger.exception("AI request failed")
        return jsonify({
            "error": "AI request failed. Check server settings."
        }), 500

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
