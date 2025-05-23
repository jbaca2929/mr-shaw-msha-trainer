import streamlit as st
import os
import openai

# Initialize OpenAI client securely
openai.api_key = os.getenv("OPENAI_API_KEY")

# Page setup
st.set_page_config(page_title="Mr. Shaw – MSHA Trainer", layout="centered")
st.title("🛠️ Ask Mr. Shaw – Your MSHA Safety Trainer")
st.caption("Powered by OpenAI. Designed with Certified MSHA Instructors.")

# Input box
question = st.text_input(
    "Ask a safety question, regulation, or training need:",
    placeholder="e.g. What’s required in hazard training for new underground miners?"
)

# Action button
if st.button("Ask Mr. Shaw") and question.strip():
    with st.spinner("🔎 Mr. Shaw is checking MSHA regulations, guidance, and sources..."):
        prompt = f"""
You are Mr. Shaw, a certified MSHA trainer with 30 years of experience. A miner asks:

"{question}"

Please respond with:
1. A concise answer (3–5 sentences)
2. The specific MSHA regulation (Part 46 or 48, cite subpart)
3. A link to an official MSHA.gov or NIOSH.gov resource
4. If helpful, include a related YouTube training video link

Use **bold labels** for: **Rule Cited**, **Source**, **Video**, etc.
Keep a practical tone and stay compliant with MSHA standards.
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
            answer = response['choices'][0]['message']['content']
            st.markdown(answer)

        except Exception as e:
            st.error(f"❌ OpenAI Error: {e}")
