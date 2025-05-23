import streamlit as st
import os
from fpdf import FPDF
import openai

# Set API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up Streamlit
st.set_page_config(page_title="Mr. Shaw – MSHA Trainer", layout="centered")
st.title("🛠️ Ask Mr. Shaw – Your MSHA Safety Trainer")
st.caption("Powered by OpenAI. Built with Certified MSHA Instructors.")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mine type input
mine_type = st.radio("Select your mine type:", [
    "Part 46 (Sand & Gravel)",
    "Part 48 Surface",
    "Part 48 Underground"
])

# Question input
question = st.text_input(
    "Ask a safety question, regulation, or training need:",
    placeholder="e.g. What’s required for fall protection under Part 48?"
)

# Chat display
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Ask button
if st.button("Ask Mr. Shaw") and question.strip():
    user_message = {"role": "user", "content": question}
    st.session_state.messages.append(user_message)

    with st.spinner("🔎 Mr. Shaw is reviewing MSHA regulations..."):
        prompt = f"""
You are Mr. Shaw, a certified MSHA trainer with 30 years of experience.

A miner from a {mine_type} site asks: "{question}"

Respond with:
1. A clear answer (3–5 sentences)
2. **Rule Cited**: Include the specific MSHA regulation (Part and subpart)
3. **Source**: Link to MSHA.gov or NIOSH.gov
4. **Video** (optional): YouTube training if available

Speak plainly, like an experienced safety coach. Cite real rules where possible.
"""
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are Mr. Shaw, an MSHA training expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4
            )
            answer = response.choices[0].message.content
            assistant_message = {"role": "assistant", "content": answer}
            st.session_state.messages.append(assistant_message)
            st.chat_message("assistant").markdown(answer)

        except Exception as e:
            st.error(f"❌ OpenAI Error: {e}")

# PDF Export (basic text file fallback)
if st.download_button(
    "📄 Export Chat as PDF",
    "\n".join([f"{m['role'].title()}: {m['content']}" for m in st.session_state.messages]),
    file_name="msha_chat_log.txt"
):
    pass

st.markdown("---\nBuilt with AI. This is not official MSHA guidance. Always verify with your Supervisor or MSHA Inspector.")
