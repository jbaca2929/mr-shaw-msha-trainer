import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"],
    organization=st.secrets.get("OPENAI_ORG_ID", None),
    project=st.secrets.get("OPENAI_PROJECT_ID", None)
)

# UI layout
st.set_page_config(page_title="Mr. Shaw – Your MSHA Trainer")
st.title("👷 Mr. Shaw – Your MSHA Trainer")
st.markdown("""
Ask an MSHA safety question and Mr. Shaw will answer based on official CFR guidance.
""")

# Mine type selection
mine_type = st.radio(
    "Select your mine type:",
    [
        "Part 46 – Sand & Gravel",
        "Part 48 – Surface Mine",
        "Part 48 – Underground Mine"
    ]
)

# Custom or common question inputs
custom_question = st.text_input("Type your MSHA safety question:", placeholder="e.g. What is required PPE?")
common_question = st.selectbox("Or choose a common question:", [
    "",
    "What are my miners' rights?",
    "What is fall protection?",
    "What is required PPE?",
    "What is a workplace examination?",
    "What training do new miners need?"
])

# Ask button logic
if st.button("Ask Mr. Shaw"):
    final_question = custom_question if custom_question.strip() else common_question

    if not final_question or final_question.strip() == "":
        st.warning("Please enter or select a question first.")
    else:
        with st.spinner("Mr. Shaw is reviewing the CFR..."):
            system_prompt = f"""
You are Mr. Shaw, a certified MSHA instructor with over 30 years of experience. When a miner asks a safety question,
you respond as a structured field instructor—not a chatbot. You teach clearly, use proper headings, cite the correct CFRs,
and guide them like they’re in training.

Use this format for your reply:
------------------------------
🟦 **Module Title: [Insert Topic]**

🎙️ **Voice Prompt**: “...” ← Say this out loud to introduce the topic.

### 📍 What to Do or Where to File
- Bullet points with clear actions
- Emphasize steps in bold
- Use real links like [MSHA.gov](https://www.msha.gov)

### 📝 Information Needed
- Bullet points
- Be specific and practical

📘 **CFR Reference**: Include exact 30 CFR or Mine Act citation

🎙️ **Voice Prompt**: “...” ← A closing reminder in voice style
------------------------------

Only use MSHA standards—not OSHA. Do not generalize fall protection, training, or safety requirements unless explicitly cited in 30 CFR.

This miner is working under: {mine_type}
"""

            try:
                response = client.chat.completions.create(
                    model="gpt-4",  # use "gpt-3.5-turbo" if needed for access
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": final_question}
                    ]
                )
                answer = response.choices[0].message.content
                st.success("Mr. Shaw says:")
                st.markdown(answer)
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Footer disclaimer
st.markdown("""
---
**Disclaimer:** Mr. Shaw is an AI-powered assistant. While he draws on official MSHA CFR sources to provide guidance, 
his responses are not a substitute for formal training, legal advice, or direct MSHA consultation. 
Always verify compliance with a certified instructor or MSHA official.
""")
