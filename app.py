from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    organization=os.environ.get("OPENAI_ORG_ID"),  # optional, can remove
    project=os.environ.get("OPENAI_PROJECT_ID")     # required for sk-proj keys
)

@app.route("/ask-mr-shaw", methods=["POST"])
def ask_mr_shaw():
    data = request.json
    question = data.get("question", "").strip()
    mine_type = data.get("mine_type", "").strip()

    if not question:
        return jsonify({"error": "Missing question"}), 400
    if not mine_type:
        return jsonify({"error": "Missing mine type"}), 400

    # Set CFR restriction rules
    if "Part 46" in mine_type:
        allowed_cfr = "Only cite regulations from 30 CFR Part 46. Do not include references to Part 48 or Part 56."
    elif "Underground" in mine_type:
        allowed_cfr = "Only cite regulations from 30 CFR Part 48 Subpart A. Do not include references to Part 46 or Part 56."
    else:
        allowed_cfr = "Only cite regulations from 30 CFR Part 48 Subpart B. Do not include references to Part 46 or Part 56."

    system_prompt = (
        f"You are Mr. Shaw, a certified MSHA instructor with 30+ years of field experience. "
        f"Respond using official CFR standards only.\n"
        f"The miner works under: {mine_type}.\n"
        f"{allowed_cfr}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4",  # use "gpt-4" or "gpt-3.5-turbo" depending on access
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ]
        )
        answer = response.choices[0].message.content.strip()
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
