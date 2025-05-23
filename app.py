import streamlit as st
from openai import OpenAI
from datetime import datetime
from utils import get_simulated_context, format_response

# Page settings
st.set_page_config(page_title="Mr. Shaw MSHA Trainer", layout="centered")
st.title("👷‍♂️ Mr. Shaw MSHA Trainer")
st.markdown("**MSHA-compliant safety guidance from a certified instructor—just ask.**")

# Load OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Session memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Mine type
mine_type = st.radio("🛠️ What type of mine are you working on?", [
    "Part 46 – Sand & Gravel",
    "Part 48 – Surface Mine",
    "Part 48 – Underground Mine"
])

# Training topic buttons (optional)
st.markdown("### 🧭 Choose a topic or ask your own question:")
cols = st.columns(5)
topics = ["Equipment Safety", "Emergency", "Handling", "HazCom", "Fall Prot."]
for i, topic in enumerate(topics):
    with cols[i]:
        st.button(f"📌 {topic}", key=f"topic_{i}")

# User question
st.markdown("### ✏️ What’s your safety question today?")
user_question = st.text_input("Type your question below:", placeholder="e.g., What are the rules for fall protection?")
st.button("🎤 Speak (voice input coming soon)", disabled=True)

# Ask Mr. Shaw
if st.button("🔵 Ask Mr. Shaw") and user_question:
    with st.spinner("Mr. Shaw is reviewing the CFR..."):

        # Retrieve simulated MSHA context (placeholder for future RAG)
        doc = get_simulated_context(user_question)
        context = doc["snippet"] if doc else "No matching MSHA snippet found. Providing general guidance."

        # Prompt structure
        system_prompt = f"""
You are Mr. Shaw, a certified MSHA instructor with 30+ years of experience. Speak like you're training real miners—direct, clear, and legally correct.

- Summarize in plain language
- Quote the regulation when appropriate
- Always cite MSHA/NIOSH/CFR officially (e.g., 30 CFR § 56.15005)
- Use the mine type context: {mine_type}
- Context from MSHA documents: {context}
"""

        # OpenAI call
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

        except Exception as e:
            st.error("❌ GPT-4 API call failed:")
            st.code(str(e))

# Display response history
if st.session_state.chat_history:
    st.markdown("## 📚 Mr. Shaw's Responses")
    for idx, (q, a) in enumerate(reversed(st.session_state.chat_history)):
        st.markdown(f"**🗨️ Question:** {q}")
        st.markdown(a)
        st.divider()

# Footer
st.warning("⚠️ Always follow your site-specific safety plan and consult with a certified trainer.")
st.caption(f"App version 1.0 — Updated {datetime.now().strftime('%b %d, %Y')}")
