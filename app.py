import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Mr. Shaw – MSHA Trainer")
st.title("👷 Mr. Shaw – MSHA Trainer")
st.write("Ask an MSHA safety question and Mr. Shaw will answer based on official CFR guidance.")

# Initialize OpenAI with API key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# UI
mine_type = st.selectbox("Select your mine type:", [
    "Part 46 – Sand & Gravel", 
    "Part 48 – Surface Mine", 
    "Part 48 – Underground Mine"
])

question = st.text_input("What is your MSHA safety question?")
submit = st.button("Ask Mr. Shaw")

if submit and question:
    with st.spinner("Mr. Shaw is reviewing the CFR..."):
        try:
            system_prompt = f"""
You are Mr. Shaw, a certified MSHA instructor with 30+ years of experience. 
Only cite regulations from MSHA.gov or 30 CFR. The user works under {mine_type}.
Speak clearly, practically, and professionally.
"""

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ]
            )
            st.markdown(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Error: {e}")
elif submit:
    st.warning("Please type a question before submitting.")
