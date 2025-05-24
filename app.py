import streamlit as st
from openai import OpenAI

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"],
    organization=st.secrets.get("OPENAI_ORG_ID", None),
    project=st.secrets.get("OPENAI_PROJECT_ID", None)
)


# App title and intro
st.title("👷 Mr. Shaw – MSHA Trainer")
st.write("""
Ask an MSHA safety question and Mr. Shaw will answer based on official CFR guidance.
""")

# Select mine type
mine_type = st.selectbox(
    "Select your mine type:",
    ["Part 46 – Sand & Gravel", "Part 48 – Surface Mine", "Part 48 – Underground Mine"]
)

# User question
user_question = st.text_input("What is your MSHA safety question?")

# Submit
if st.button("Ask Mr. Shaw"):
    if not user_question:
        st.warning("Please enter a question before submitting.")
    else:
        with st.spinner("Mr. Shaw is reviewing the CFR..."):
            system_prompt = f"""
            You are Mr. Shaw, a certified MSHA instructor with 30+ years of field experience.
            Answer this safety question in detail based on MSHA CFR guidelines.
            Be clear, practical, and include citations when possible.
            The miner works in this environment: {mine_type}
            """

            try:
                response = client.chat.completions.create(
                    model="gpt-4.1",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_question}
                    ]
                )
                answer = response.choices[0].message.content
                st.success("Mr. Shaw says:")
                st.write(answer)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
