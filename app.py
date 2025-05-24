import streamlit as st
from openai import OpenAI

# Set up OpenAI client using Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Mr. Shaw – MSHA Trainer", layout="centered")

st.title("👷 Mr. Shaw – MSHA Trainer")
st.markdown("Ask an MSHA safety question and Mr. Shaw will answer based on official CFR guidance.")

# Dropdown for mine type
mine_type = st.selectbox("Select your mine type:", [
    "Part 46 – Sand & Gravel",
    "Part 48 – Surface Mine",
    "Part 48 – Underground Mine"
])

# Text input for safety question
user_question = st.text_input("What is your MSHA safety question?")

# Button to submit question
if st.button("Ask Mr. Shaw") and user_question:
    with st.spinner("Mr. Shaw is reviewing the CFR..."):

        # Build the prompt
        system_prompt = f"""
        You are Mr. Shaw, a certified MSHA instructor with over 30 years of experience.
        Respond clearly and accurately based on current CFR regulations.
        The user is asking about safety requirements at a {mine_type}.
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

            answer = response.choices[0].message.content
            st.markdown("### ✅ Mr. Shaw says:")
            st.write(answer)

        except Exception as e:
            st.error(f"Something went wrong: {e}")
