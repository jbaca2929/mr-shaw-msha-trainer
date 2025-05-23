import streamlit as st
import os
import openai
from fpdf import FPDF
import base64
from openai import OpenAI

# Set API key securely from environment
openai.api_key = os.getenv("OPENAI_API_KEY")



# Initialize session state for chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Page setup
st.set_page_config(page_title="Mr. Shaw – MSHA Trainer", layout="centered")
st.title("🛠️ Ask Mr. Shaw – Your MSHA Safety Trainer")
st.caption("Powered by OpenAI. Built with Certified MSHA Instructors.")

# Mine type selector
mine_type = st.selectbox("Select your mine type:", ["Part 46 (Sand & Gravel)", "Part 48 Surface", "Part 48 Underground"])

# Input
question = st.text_input("Ask a safety question, regulation, or training need:", placeholder="e.g. What’s required in hazard training for new miners?")

# Display conversation history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Ask Mr. Shaw
if st.button("Ask Mr. Shaw") and question.strip():
    user_msg = {"role": "user", "content": question.strip()}
    st.session_state.messages.append(user_msg)
    with st.spinner("🔎 Mr. Shaw is reviewing MSHA regulations..."):
        prompt = f"""
You are Mr. Shaw, a certified MSHA trainer with 30 years of experience.
A miner from a {mine_type} site asks: \"{question}\"

Provide:
1. A concise answer (3–5 sentences)
2. The **specific MSHA regulation** (Part and subpart)
3. A trusted MSHA.gov or NIOSH.gov resource
4. Optional: YouTube link to a relevant training video

Use **bold headings** for **Rule Cited**, **Source**, etc. Keep it clear and compliant.
"""
        try:
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

# PDF Export
if st.download_button("📄 Export Chat as PDF", "\n".join([f"{m['role'].title()}: {m['content']}" for m in st.session_state.messages]), file_name="msha_chat_log.txt"):
    pass

# Optional: TTS export (placeholder for future voice support)
# You can integrate pyttsx3 or an audio stream to download a spoken version of the answer

st.markdown("""
---
Built with AI. This is not official MSHA guidance. Always verify with your inspector.
""")
