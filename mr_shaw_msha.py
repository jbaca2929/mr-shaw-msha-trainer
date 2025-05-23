import streamlit as st
import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Page setup
st.set_page_config(page_title="Mr. Shaw 🛠️ MSHA Expert Safety Coach", layout="centered")
st.title("🛠️ Ask Mr. Shaw – Your MSHA Safety Trainer")
st.caption("Powered by OpenAI. Designed with Certified MSHA Instructors.")

# Input
question = st.text_input(
    "Ask a safety question, regulation, or training need:",
    placeholder="e.g. What’s required in hazard training for new underground miners?"
)

# Button + Action
if st.button("Ask Mr. Shaw") and question:
    with st.spinner("Checking MSHA rules, studies, and trusted sources..."):
        prompt = f"""
You are Mr. Shaw, a certified MSHA trainer with 30 years of experience in surface and underground mining.

A miner has asked: "{question}"

Respond with:
1. A clear answer (3–5 sentences)
2. The applicable MSHA regulation (specify Part 46 or 48 and cite the subpart or rule)
3. 1 official MSHA.gov or NIOSH.gov link (resource, study, or training guide)
4. If helpful, include a trusted YouTube link from MSHA or NIOSH

Format your answer like a conversation from Mr. Shaw. Do not sound like ChatGPT.
Use **bold labels** like **Rule Cited**, **Source**, and **Video** to organize your reply.
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are Mr. Shaw, an MSHA expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4
            )

            answer = response.choices[0].message.content
            st.markdown(answer)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Footer
st.markdown("""
---
Built with 💡 by MSHA safety professionals. Not official MSHA guidance. Always verify with your Supervisor or MSHA Inspector.
""")
