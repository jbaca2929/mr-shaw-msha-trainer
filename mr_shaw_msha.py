import streamlit as st
import os
from openai import OpenAI
from fpdf import FPDF

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Session state for persistent chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Streamlit UI
st.set_page_config(page_title="Mr. Shaw – MSHA Trainer", layout="centered")
st.title("🛠️ Ask Mr. Shaw – Your MSHA Safety Trainer")
st.caption("Powered by OpenAI. Built with Certified MSHA Instructors.")

# Mining type selection
mine_type = st.selectbox("Select your mine type:", ["Part 46 (Sand & Gravel)", "Part 48 Surface", "Part 48 Underground"])

# Question input
question = st.text_input("Ask a safety question, regulation, or training need:", placeholder="e.g. What’s required in hazard training for new miners?")

# Chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Process question
if st.button("Ask Mr. Shaw") and question.strip():
    user_msg = {"role": "user", "content": question.strip()}
    st.session_state.messages.append(user_msg)

    with st.spinner("🔎 Mr. Shaw is reviewing MSHA regulations..."):
        prompt = f"""
You are Mr. Shaw, a certified MSHA trainer with 30 years of experience.
A miner from a {mine_type} site asks: \"{question}\"

Please respond with:
1. A concise answer (3–5 sentences)
2. The **specific MSHA regulation** (Part and subpart)
3. A trusted MSHA.gov or NIOSH.gov resource
4. Optional: YouTube link to a relevant training video

Use **bold headings** for **Rule Cited**, **Source**, etc.
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are Mr. Shaw, an MSHA training expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4
            )
            answer = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.chat_message("assistant").markdown(answer)

        except Exception as e:
            st.error(f"❌ OpenAI Error: {e}")

# Export as PDF
if st.download_button("📄 Export Chat as PDF", "\n\n".join([f"{m['role'].title()}: {m['content']}" for m in st.session_state.messages]), file_name="msha_chat_log.txt"):
    pass

st.markdown("---\nBuilt with AI. This is not official MSHA guidance. Always verify with your inspector.")
