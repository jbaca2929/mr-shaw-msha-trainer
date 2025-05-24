import streamlit as st
from openai import OpenAI

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"],
    organization=st.secrets.get("OPENAI_ORG_ID", None),
    project=st.secrets.get("OPENAI_PROJECT_ID", None)
)

st.set_page_config(page_title="Mr. Shaw – Your MSHA Trainer")
st.title("👷 Mr. Shaw – Your MSHA Trainer")
st.markdown("""
Ask an MSHA safety question and Mr. Shaw will answer based on official CFR guidance.
""")

mine_type = st.radio(
    "Select your mine type:",
    [
        "Part 46 – Sand & Gravel",
        "Part 48 – Surface Mine",
        "Part 48 – Underground Mine"
    ]
)

question_options = [
    "What are my miners' rights?",
    "What is fall protection?",
    "What is required PPE?",
    "What is a workplace examination?",
    "What training do new miners need?"
]

selected_question = st.radio("Or choose a common question:", question_options)

# Autofill the text input field based on selected radio question
custom_question = st.text_input(
    "Or type your own MSHA safety question:",
    value=selected_question if selected_question else ""
)

submit = st.button("Ask Mr. Shaw")

if submit and custom_question:
    user_question = custom_question
    with st.spinner("Mr. Shaw is reviewing the CFR..."):
        system_prompt = f"""
        You are Mr. Shaw, a certified MSHA instructor with 30+ years of field experience.
        Answer this safety question in detail based strictly on MSHA CFR guidelines. Not OSHA.
        Never mention fall protection at 4 feet unless explicitly cited in CFR.
        Be clear, practical, and include citations when possible.
        The user is working under: {mine_type}
        """

        response = client.chat.completions.create(
            model="gpt-4.1-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ]
        )

        st.success("Mr. Shaw says:")
        st.write(response.choices[0].message.content)

st.markdown("""
---
**Disclaimer:** Mr. Shaw is an AI-powered assistant. While he draws on official MSHA CFR sources to provide guidance, his responses are not a substitute for formal training, legal advice, or direct MSHA consultation. Always verify compliance with a certified instructor or MSHA official.
""")
