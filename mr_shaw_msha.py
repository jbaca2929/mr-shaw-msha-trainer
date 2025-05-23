import streamlit as st
import os
from fpdf import FPDF
from openai import OpenAI

# Initialize OpenAI client (v1.0+ syntax)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set up Streamlit
st.set_page_config(page_title="Mr. Shaw – MSHA Trainer", layout="centered")
st.title("🛠️ Ask Mr. Shaw – Your MSHA Safety Trainer")
st.caption("Powered by OpenAI. Built with Certified MSHA Instructors.")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mine type selector
mine_type = st.radio("Select your mine type:", [
    "Part 46 (Sand & Gravel)",
    "Part 48 Surface",
    "Part 48 Underground"
])

# User input
question = st.text_input(
    "Ask a safety question, regulation, or training need:",
    placeholder="e.g. What is fall protection?"
)

# Display chat
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Ask Mr. Shaw
if st.button("Ask Mr. Shaw") and question.strip():
    user_msg = {"role": "user", "content": question.strip()}
    st.session_state.messages.append(user_msg)

    with st.spinner("🔎 Mr. Shaw is reviewing MSHA regulations..."):
        try:
            prompt = f"""
You are Mr. Shaw, a certified MSHA trainer with 30 years of experience.
A miner from a {mine_type} site asks: "{question}"

Respond with:
1. A clear answer (3–5 sentences)
2. **Rule Cited**: Include the specific MSHA regulation (Part and subpart)
3. **Source**: Link to MSHA.gov or NIOSH.gov
4. **Video** (optional): YouTube training if applicable

Speak plainly like a seasoned trainer. Cite real regulations when possible.
"""

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

# Export chat to PDF (as .txt fallback)
if st.download_button("📄 Export Chat as PDF", "\n".join([f"{m['role'].title()}: {m['content']}" for m in st.session_state.messages]), file_name="msha_chat_log.txt"):
    pass

# Footer
st.markdown("---\n🔒 Built with AI. This is not official MSHA guidance. Always verify with your inspector.")

