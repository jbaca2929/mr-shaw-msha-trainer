import streamlit as st
import openai
import os

# --- Page Config ---
st.set_page_config(page_title="Mr. Shaw – MSHA Trainer", layout="centered")
st.title("🛠️ Ask Mr. Shaw – Your MSHA Safety Trainer")
st.caption("Powered by OpenAI. Designed with Certified MSHA Instructors.")

# --- Input Box ---
question = st.text_input(
    "Ask a safety question, regulation, or training need:",
    placeholder="e.g. What’s required in hazard training for new underground miners?"
)

# --- Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display previous messages ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Submit Question ---
if st.button("Ask Mr. Shaw") and question.strip():
    with st.spinner("🔎 Mr. Shaw is checking MSHA regulations, guidance, and sources..."):
        user_msg = {"role": "user", "content": question}
        st.session_state.messages.append(user_msg)

        # --- Prompt Setup ---
        system_msg = {
            "role": "system",
            "content": (
                "You are Mr. Shaw, a certified MSHA trainer with 30 years of experience."
                " When a miner asks a question, you respond with:"
                "\n1. A concise 3–5 sentence explanation"
                "\n2. The MSHA regulation (cite Part 46 or 48 + subpart)"
                "\n3. A trusted MSHA.gov or NIOSH.gov source"
                "\n4. A related YouTube training link if relevant"
                "\n\nUse bold labels like **Rule Cited**, **Source**, **Video**, and keep a professional but helpful tone."
            )
        }

        try:
            openai.api_key = os.getenv("OPENAI_API_KEY")
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[system_msg] + st.session_state.messages,
                temperature=0.4,
            )
            assistant_msg = response["choices"][0]["message"]
            st.session_state.messages.append(assistant_msg)

            with st.chat_message("assistant"):
                st.markdown(assistant_msg["content"])

        except Exception as e:
            st.error(f"❌ OpenAI Error: {e}")

# --- Footer ---
st.markdown("---")
st.caption("Built with 💡 by MSHA safety professionals. Not official MSHA guidance. Always verify with your Supervisor or MSHA Inspector.")
