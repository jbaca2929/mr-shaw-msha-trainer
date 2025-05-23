import streamlit as st
import os
import openai

# --- Page Config ---
st.set_page_config(page_title="Mr. Shaw – MSHA Trainer", layout="centered")
st.title("🛠️ Ask Mr. Shaw – Your MSHA Safety Trainer")
st.caption("Powered by OpenAI. Designed with Certified MSHA Instructors.")

# --- Get API Key from Environment ---
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- Input UI ---
question = st.text_input(
    "Ask a safety question, regulation, or training need:",
    placeholder="e.g. What’s required for fall protection in surface mining?"
)

submit = st.button("Ask Mr. Shaw")

# --- Handle Submission ---
if submit and question.strip():
    with st.spinner("🔎 Mr. Shaw is checking MSHA regulations, guidance, and trusted sources..."):
        prompt = f"""
You are Mr. Shaw, a certified MSHA trainer with 30 years of experience. A miner has asked:

"{question}"

Respond with:
1. A clear answer (3–5 sentences)
2. The MSHA regulation that applies (Part 46 or 48, cite the subpart or rule)
3. A trusted MSHA.gov or NIOSH.gov source link
4. Optionally, a helpful YouTube video for further training

Use **bold labels** like **Rule Cited**, **Source**, and **Video**. Keep the tone practical and professional.
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are Mr. Shaw, an MSHA training expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4
            )
            answer = response.choices[0].message.content
            st.markdown("---")
            st.markdown(answer)

        except Exception as e:
            st.error(f"❌ OpenAI Error: {e}")

# --- Footer ---
st.markdown("""
---
Built with AI. Not official MSHA guidance. Always verify with your Supervisor or MSHA Inspector.
""")

