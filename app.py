from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    organization=os.environ.get("OPENAI_ORG_ID", None),
    project=os.environ.get("OPENAI_PROJECT_ID", None)
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

    # Determine the correct CFR limitation
    if "Part 46" in mine_type:
        allowed_cfr = "Only cite regulations from 30 CFR Part 46. Do not include references to Part 48 or Part 56."
    elif "Underground" in mine_type:
        allowed_cfr = "Only cite regulations from 30 CFR Part 48 Subpart A. Do not include references to Part 46 or Part 56."
    else:
        allowed_cfr = "Only cite regulations from 30 CFR Part 48 Subpart B. Do not include references to Part 46 or Part 56."

    # Dynamic section title based on the question
    lowered_question = question.lower()
    if any(word in lowered_question for word in ["file", "report"]):
        section_title = "📨 Where to Report or File a Complaint"
    elif "right" in lowered_question:
        section_title = "🛡️ Your MSHA Rights"
    elif any(word in lowered_question for word in ["how", "do i", "steps"]):
        section_title = "📍 Steps to Follow"
    elif any(word in lowered_question for word in ["what is", "define", "tell me"]):
        section_title = "📘 What You Need to Know"
    elif any(word in lowered_question for word in ["requirement", "need", "mandatory"]):
        section_title = "📋 MSHA Requirements"
    else:
        section_title = "📌 Guidance Based on CFR"

    system_prompt = f"""
You are Mr. Shaw, a certified MSHA instructor with 30+ years of field experience.
Respond using official CFR standards only.
The miner works under: {mine_type}.
{allowed_cfr}

Respond in this markdown format:

🟦 **Module Title: {question}**

### {section_title}
- Bullet list of clear, practical answers

### 📝 Information Needed
- List any documentation, records, or training miners should maintain

📘 **CFR Reference**: Include specific CFR citations only from the allowed part

---

🔎 **Disclaimer:** This response is for informational purposes only. It does not replace formal MSHA training, legal interpretation, or compliance obligations. Always confirm with a certified MSHA trainer or inspector.
""".strip()

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ]
        )
        answer = response.choices[0].message.content.strip()
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
