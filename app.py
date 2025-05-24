import streamlit as st
from openai import OpenAI

# Load OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set Streamlit page config (this MUST be first!)
st.set_page_config(page_title="Mr. Shaw – MSHA Trainer")

# Title and description
st.title("👷 Mr. Shaw – MSHA Trainer")
st.write("MSHA-compliant safety guidance from a certified instructor—just ask.")

# Mine type selector
mine_type = st.radio("🔧 What type of mine are you working on?", [
    "Part 46 – Sand & Gravel",
    "Part 48 – Surface Mine",
    "Part 48 – Underground Mine"
])

# User input
user_question = st.text_input("Type your MSHA safety question:")
submit = st.button("🔵 Ask Mr. Shaw")

# Handle question submit
if submit and user_question:
    with st.spinner("🔍 Mr. Shaw is reviewing the CFR..."):

        # Build system prompt
        system_prompt = f"""
You are Mr. Shaw, a certified MSHA instructor with 30+ years of field experience.
Speak like you're training real miners—direct, practical, and legally correct.

- Summarize in plain terms
- Quote the regulation when relevant
- Always cite MSHA/NIOSH/CFR officially (e.g., 30 CFR § 56.15005)
- Mine Type: {mine_type}
- Question: {user_question}
"""

        try:
            # GPT-4 call
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_question}
                ],
                temperature=0.3
            )
            ai_output = response.choices[0].message.content.strip()

            # Display answer
            st.success("✅ Mr. Shaw responded:")
            st.write(ai_output)

        except Exception as e:
            st.error("❌ GPT-4 failed:")
            st.code(str(e))

# Footer
st.caption("App version 1.0 — Powered by OpenAI + Streamlit")
