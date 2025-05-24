import streamlit as st
from openai import OpenAI

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"],
    organization=st.secrets.get("OPENAI_ORG_ID", None),
    project=st.secrets.get("OPENAI_PROJECT_ID", None)
)

st.set_page_config(page_title="Mr. Shaw – Your MSHA Trainer")
st.title("👷 Mr. Shaw – MSHA Trainer")
st.markdown("""
Ask an MSHA safety question and Mr. Shaw will answer based on official CFR guidance.
""")

mine_type = st.radio(
    "Select your mine type:",
    [
        "Part 46 – Sand & Gravel",
        "Part 48 – Surface Mine",
        "Part 48 – Underground Mine"
    ],
    index=0
)

predefined_questions = [
    "What are my miners' rights?",
    "What is fall protection?",
    "What are the workplace examination requirements?",
    "What PPE is required for miners?",
    "What are the training requirements under Part 46 or 48?"
]

question = st.selectbox("What is your MSHA safety question?", predefined_questions + ["Other – I'll type my own question"])

custom_question = ""
if question == "Other – I'll type my own question":
    custom_question = st.text_input("Type your custom MSHA safety question:")

submit = st.button("Ask Mr. Shaw")

final_question = custom_question if question == "Other – I'll type my own question" else question

if submit and final_question:
    with st.spinner("Mr. Shaw is reviewing the CFR..."):
        system_prompt = f"""
        You are Mr. Shaw, a certified MSHA instructor with 30+ years of field experience.
        Answer this safety question in detail based strictly on MSHA CFR guidelines.Not OSHA.
        Never mention fall protection at 4 feet unless explicitly cited in CFR.
        Be clear, practical, and include citations when possible.
        The user is working under: {mine_type}
        """

        completion = client.chat.completions.create(
            model="gpt-4.1-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": final_question}
            ]
        )

        st.success("Mr. Shaw says:")
        st.write(completion.choices[0].message.content)

st.markdown("""
---
**Disclaimer:** Mr. Shaw is an AI-powered assistant. While he draws on official MSHA CFR sources to provide guidance, his responses are not a substitute for formal training, legal advice, or direct MSHA consultation. Always verify compliance with a certified instructor or MSHA official.
""")
