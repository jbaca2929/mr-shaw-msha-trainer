import streamlit as st
from openai import OpenAI
from datetime import datetime
from utils import get_simulated_context, format_response

# Streamlit page setup
st.set_page_config(page_title="Mr. Shaw MSHA Trainer", layout="centered")
st.title("👷‍♂️ Mr. Shaw MSHA Trainer")
st.markdown("**MSHA-compliant safety guidance from a certified instructor—just ask.**")

# Load API key from secrets (managed via GitHub or Streamlit Cloud)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Mine type
mine_type = st.radio("🛠️ What type of mine are you working on?",
                     ["Part 46 – Sand & Gravel", "Part 48 – Surface Mine", "Part 48 – Underground Mine"])

# Topic tags
st.markdown("### 🧭 Choose a topic or ask your own question:")
cols = st.columns(5)
topics = ["Equipment Safety", "Emergency", "Handling", "HazCom", "Fall Prot."]
for i, topic in enumerate(topics):
    with cols[i]:
        if st.button(f"📌 {topic}", key=f"topic_{i}"):
            st.session_state.selected_topic = topic

# Question input
st.markdown("### ✏️ What’s your safety question today?")
user_question = st.text_input("Type your question below:", placeholder="e.g., What are the rules for respirator use in underground mines?")

# Ask Mr. Shaw
if st.button("🔵 Ask Mr. Shaw") and user_question:
    with st.spinner("Mr. Shaw is reviewing the CFR..."):

        # Simulated RAG context (upgrade to FAISS later)
        doc = get_simulated_context(user_question)
        context = doc["snippet"] if doc else "No exact document found. Defaulting to general MSHA instruction."

        # System prompt
        system_prompt = f"""
You are Mr. Shaw, a certified MSHA instructor with 30+ years of field experience. Speak like you're training real miners—direct, practical, and legally correct.

- Summarize in plain terms
- Quote the regulation when relevant
- Always cite MSHA/NIOSH/CFR officially (e.g., 30 CFR § 56.11003)
- Use the mine type context: {mine_type}
- Context from MSHA docs: {context}
"""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ],
            temperature=0.3
        )

        # Output formatting
        ai_output = response.choices[0].message.content.strip()
        formatted = format_response(ai_output, doc)

        # Save in history
        st.session_state.chat_history.append((user_question, formatted))

# Display chat history
if st.session_state.chat_history:
    st.markdown("## 📚 Mr. Shaw's Responses")
    for idx, (q, a) in enumerate(reversed(st.session_state.chat_history)):
        st.markdown(f"**🗨️ Question:** {q}")
        st.markdown(a)
        st.divider()

st.write("🛠️ Triggered the Mr. Shaw response!")




# Footer
st.warning("⚠️ Always follow your site-specific safety plan and consult with a certified trainer.")
st.caption(f"App version 1.0 — Updated {datetime.now().strftime('%b %d, %Y')}")
