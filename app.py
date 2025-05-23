import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Mr. Shaw – MSHA Trainer", layout="centered")
st.title("👷‍♂️ Mr. Shaw – MSHA Trainer")
st.markdown("MSHA-compliant safety guidance from a certified instructor—just ask.")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Mine type selector
mine_type = st.radio("🛠️ What type of mine are you working on?", [
    "Part 46 – Sand & Gravel",
    "Part 48 – Surface Mine",
    "Part 48 – Underground Mine"
])

# Text input
user_question = st.text_input("Type your MSHA safety question:")

# Submit button
if st.button("🔵 Ask Mr. Shaw") and user_question.strip():
    st.write(f"**Question:** {user_question}")
    st.write(f"**Mine Type:** {mine_type}")

    with st.spinner("🧠 Mr. Shaw is reviewing the CFR..."):
        try:
            # Hardcoded test response to isolate GPT issues
            st.success("✅ Mr. Shaw responded:")
            ai_output = (
                "MSHA requires fall protection whenever miners are exposed to falling more than 6 feet. "
                "Regulation: 30 CFR § 56.15005."
            )
            st.markdown(ai_output)
        except Exception as e:
            st.error("❌ Error during fallback response:")
            st.code(str(e))

# Footer
st.caption("App version 1.0 — Debug Mode Enabled")
