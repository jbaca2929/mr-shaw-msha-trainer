import streamlit as st
from openai import OpenAI
from datetime import datetime
from utils import get_simulated_context, format_response

# Page setup
st.set_page_config(page_title="Mr. Shaw MSHA Trainer", layout="centered")
st.title("👷‍♂️ Mr. Shaw MSHA Trainer")
st.markdown("**MSHA-compliant safety guidance from a certified instructor—just ask.**")

# OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = ""
if "submit" not in st.session_state:
    st.session_state.submit = False

# Mine type selection
mine_type = st.radio("🛠️ What type of mine are you working on?", [
    "Part 46 – Sand & Gravel",
    "Part 48 – Surface Mine",
    "Part 48 – Underground Mine"
])

# Topics
topics = {
    "Equipment Safety": "What are the MSHA requirements for equipment safety?",
    "Emergency": "What are MSHA's emergency response rules?",
    "Handling": "What are safe material handling procedures under MSHA?",
    "Workplace Exams": "What does MSHA require for workplace exams?",
    "HazCom": "What is required for hazard communication under MSHA?",
    "Fall Protection": "What are MSHA's rules for fall protection?"
}

# Topic buttons
st.markdown("### 🧭 Choose a topic or ask your own question:")
cols = st.columns(len(topics))
for i, (label, question) in enumerate(topics.items()):
    with cols[i]:
        if st.button(f"📌 {label}", key=f"topic_{i}_{label}"):
            st.session_state.selected_topic = question

# Question input
st.markdown("### ✏️ What’s your safety question today?")
user_question = st.text_input(
    label="Type your question below:",
    value=st.session_state.selected_topic,
    placeholder="e.g., What are the rules for fall protection?",
    key="user_question_input"
)

# Trigger flag
def submit_question():
    st.session_state.submit = True

st.button("🔵 Ask Mr. Shaw", on_click=submit_question)

# GPT-4 call
if st.session_state.submit and user_question:
    with st.spinner("Mr. Shaw is reviewing the CFR..."):
        doc = get_simulated_context(user_question)
        context = doc["snippet"] if doc else "No document matched. Providing general MSHA guidance."

        system_prompt = f"""
You are Mr. Shaw, a certified MSHA instructor with 30+ years of field experience. Speak like you're training real miners—direct, practical, and legally correct.

- Summarize in plain terms
- Quote the regulation when relevant
- Always cite MSHA/NIOSH/CFR officially (e.g., 30 CFR § 56.15005)
- Mine Type: {mine_type}
- Context from MSHA documents: {context}
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
            ai_output = response.choices[0].message.content.strip()
            formatted = format_response(ai_output, doc)
            st.session_state.chat_history.append((user_question, formatted))
            st.session_state.submit = False

        except Exception as e:
            st.error("❌ GPT-4 API call failed:")
            st.code(str(e))

# Display responses
if st.session_state.chat_history:
    st.markdown("## 📚 Mr. Shaw's Responses")
    for idx, (q, a) in enumerate(reversed(st.session_state.chat_history)):
        st.markdown(f"**🗨️ Question:** {q}")
        st.markdown(a)
        st.divider()

# Footer
st.warning("⚠️ Always follow your site-specific safety plan and consult with a certified trainer.")
st.caption(f"App version 1.0 — Updated {datetime.now().strftime('%b %d, %Y')}")
