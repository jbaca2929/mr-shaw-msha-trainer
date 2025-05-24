import streamlit as st
from openai import OpenAI

# Load OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# MUST be first
st.set_page_config(page_title="Mr. Shaw – MSHA Trainer")

# App title
st.title("👷 Mr. Shaw – MSHA Trainer")
st.write("MSHA-compliant safety guidance from a certified instructor—just ask.")

# Mine type selector
mine_type = st.radio("🔧 What type of mine are you working on?", [
    "Part 46 – Sand & Gravel",
    "Part 48 – Surface Mine",
    "Part 48 – Underground Mine"
])

# Input + Button
user_question = st.text_input("Type your MSHA safety question:")
submit = st.button("🔵 Ask Mr. Shaw")

# Always show debug values to verify logic flow
st.markdown("### 🪪 Debug info:")
st.write("Mine type:", mine_type)
st.write("Question entered:", user_question)
st.write("Submit clicked:", submit)

# GPT logic
if submit and user_question:
    st.info("⏳ Submitting to GPT-4...")

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
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ],
            temperature=0.3
        )
        output = response.choices[0].message.content.strip()
        st.success("✅ Mr. Shaw responded:")
        st.markdown(output)

    except Exception as e:
        st.error("❌ GPT-4 failed.")
        st.code(str(e))

st.caption("App version 1.0 — Debug mode enabled")
