# streamlit_test.py

import streamlit as st
import requests

st.set_page_config(page_title="Mr. Shaw – MSHA Trainer", layout="centered")

st.title("👷 Mr. Shaw – Your MSHA Trainer (Live Test)")

st.markdown("Ask any MSHA safety question below and get CFR-compliant guidance instantly.")

# Input fields
mine_type = st.radio("Select your mine type:", [
    "Part 46 – Sand & Gravel",
    "Part 48 – Surface Mine",
    "Part 48 – Underground Mine"
])

question = st.text_input("Your MSHA safety question:")

if st.button("Ask Mr. Shaw"):
    if not question:
        st.warning("Please enter a question.")
    else:
        with st.spinner("Mr. Shaw is reviewing the CFR..."):
            response = requests.post(
                "https://mr-shaw-msha-trainer.onrender.com/ask-mr-shaw",
                headers={"Content-Type": "application/json"},
                json={
                    "question": question,
                    "mine_type": mine_type
                }
            )
            if response.status_code == 200:
                st.success("Mr. Shaw says:")
                st.markdown(response.json()["answer"])
            else:
                st.error("Something went wrong: " + response.text)
