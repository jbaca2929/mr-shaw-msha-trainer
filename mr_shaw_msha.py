import streamlit as st
import os
import json
from openai import OpenAI

# Initialize OpenAI client using environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Page setup
st.set_page_config(page_title="Mr. Shaw 🛠️ MSHA Expert Safety Coach", layout="centered")
st.title("🛠️ Ask Mr. Shaw – Your MSHA Safety Trainer")
st.caption("Powered by OpenAI. Designed with Certified MSHA Instructors.")

# Input field
question = st.text_input("Ask a safety question, regulation, or training need:", 
                         placeholder="e.g. What’s required in hazard training for new miners?")

# Action
if st.button("Ask Mr. Shaw") and question:
    with st.spinner("Checking MSHA rules, studies, and trusted sources..."):

        prompt = f"""
You are "Mr. Shaw," a certified MSHA trainer with 30 years of experience in surface and underground mines.
A miner has asked: "{question}"

Respond with:
1. A clear answer (3–5 sentences)
2. The applicable MSHA regulation (specify Part 46 or 48 and cite the subpart or rule)
3. Include 1 official MSHA.gov or NIOSH.gov link (resource, study, or training guide)
4. If helpful, include a trusted YouTube link from MSHA or NIOSH

Format your answer like a conversation from Mr. Shaw. Do not sound like ChatGPT. Add short bolded labels like **Rule Cited**, **Source**, etc.
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
            reply = response.choices[0].message.content
            st.markdown(reply)

        except Exception as e:
            st.error(f"❌ Error generating response: {e}")

# Footer
st.markdown("---")
st.caption("Built with AI. Not official MSHA guidance. Always verify with your Supervisor or MSHA Inspector.")

