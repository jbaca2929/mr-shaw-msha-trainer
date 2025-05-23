import streamlit as st
from openai import OpenAI
from utils import get_simulated_context, format_response

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
        # Simulated doc retrieval
        doc = get_simulated_context(user_question)
        context = doc["snippet"] if doc and "snippet" in doc else "No document matched. Providing general MSHA guidance."

        # Prompt construction
        system_prompt = f"""
You are Mr. Shaw, a certified MSHA instructor with 30+ years of field experience. Speak like you're training real miners—direct, practical, and legally correct.

- Summarize in plain terms
- Quote the regulation when relevant
- Always cite MSHA/NIOSH/CFR officially (e.g., 30 CFR § 56.15005)
- Mine Type: {mine_type}
- Context from MSHA documents: {context}
"""

       try:
    st.success("✅ Mr. Shaw responded:")
    ai_output = f"MSHA requires fall protection whenever miners are exposed to falling more than 6 feet. Regulation: 30 CFR § 56.15005."
    st.markdown(ai_output)
 

        except Exception as e:
            st.error("❌ GPT-4 API call failed or timed out:")
            st.code(str(e))

# Footer
st.caption("App version 1.0 — Debug Mode Enabled")
