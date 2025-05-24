import streamlit as st
import requests

st.set_page_config(page_title="Mr. Shaw – MSHA Tester")

st.title("🧪 Mr. Shaw – MSHA API Tester")
st.markdown("Test your deployed API visually using this Streamlit interface.")

# --- Input form
with st.form("question_form"):
    question = st.text_input("Your MSHA Safety Question:", placeholder="e.g. What is required PPE?")
    mine_type = st.selectbox("Mine Type:", [
        "Part 46 – Sand & Gravel",
        "Part 48 – Surface Mine",
        "Part 48 – Underground Mine"
    ])
    submitted = st.form_submit_button("Ask Mr. Shaw")

# --- On submit
if submitted:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        st.info("⏳ Sending question to Mr. Shaw...")
        try:
            response = requests.post(
                "https://mr-shaw-msha-trainer.onrender.com/ask-mr-shaw",
                headers={"Content-Type": "application/json"},
                json={
                    "question": question,
                    "mine_type": mine_type
                },
                timeout=30
            )
            if response.status_code == 200:
                st.success("✅ Mr. Shaw says:")
                st.markdown(response.json().get("answer", "No answer returned."))
            else:
                st.error(f"❌ Error: {response.status_code}")
                st.code(response.text)
        except Exception as e:
            st.error(f"Request failed: {e}")
