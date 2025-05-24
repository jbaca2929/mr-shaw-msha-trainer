import streamlit as st
from openai import OpenAI

# Use the correct SDK 1.0+ client
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"],
    organization=st.secrets.get("OPENAI_ORG_ID", None),
    project=st.secrets.get("OPENAI_PROJECT_ID", None)
)

st.set_page_config(page_title="Mr. Shaw – Your MSHA Trainer")
st.title("👷 Mr. Shaw – Your MSHA Trainer")
st.markdown("Ask an MSHA safety question and Mr. Shaw will answer based on official CFR guidance.")

mine_type = st.radio("Select your mine type:", [
    "Part 46 – Sand & Gravel",
    "Part 48 – Surface Mine",
    "Part 48 – Underground Mine"
])

user_question = st.text_input("Type your MSHA safety question:")

if st.button("Ask Mr. Shaw"):
    if not user_question.strip():
        st.warning("Please type a question before submitting.")
    else:
        st.info("Mr. Shaw is reviewing the CFR...")

        if "Part 46" in mine_type:
            allowed_cfr = "Only cite regulations from 30 CFR Part 46. Do not include references to Part 48 or Part 56."
        elif "Underground" in mine_type:
            allowed_cfr = "Only cite regulations from 30 CFR Part 48 Subpart A. Do not include references to Part 46 or Part 56."
        else:
            allowed_cfr = "Only cite regulations from 30 CFR Part 48 Subpart B. Do not include references to Part 46 or Part 56."
