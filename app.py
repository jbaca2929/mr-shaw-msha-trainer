import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"],
    organization=st.secrets.get("OPENAI_ORG_ID", None),
    project=st.secrets.get("OPENAI_PROJECT_ID", None)
)

print("🔑 OpenAI client initialized.")

# Page config
st.set_page_config(page_title="Mr. Shaw – Your MSHA Trainer")
st.title("👷 Mr. Shaw – Your MSHA Trainer")
st.markdown("Ask an MSHA safety question and Mr. Shaw will answer based on official CFR guidance.")

# Mine type selection
mine_type = st.radio(
    "Select your mine type:",
    [
        "Part 46 – Sand & Gravel",
        "Part 48 – Surface Mine",
        "Part 48 – Underground Mine"
    ]
)

# Question input
user_question = st.text_input("Type your MSHA safety question:")

# Ask button logic
if st.button("Ask Mr. Shaw"):
    if not user_question or user_question.strip() == "":
        st.warning("Please type a question before submitting.")
    else:
        print("✅ Button clicked with question:", user_question)
        with st.spinner("Mr. Shaw is reviewing the CFR..."):
            system_prompt = f"""
You are Mr. Shaw, a certified MSHA instructor with over 30 years of experience. When a miner asks a safety question,
you respond as a structured MSHA instructor—not a chatbot. Provide clear, CFR-based training guidance.

Use this format for your response:
------------------------------
🟦 **Module Title: [Insert Topic]**

### 📍 What to Do or Where to File
- Bullet points with clear steps
- Emphasize key actions
- Use real links like [MSHA.gov](https://www.msha.gov)

### 📝 Information Needed
- List specific items or steps needed
- Explain how to complete reports, file complaints, or comply

📘 **CFR Reference**: Include the exact 30 CFR or Mine Act section

------------------------------

Only cite MSHA CFR rules—do not refer to OSHA or generalize. Always align your answer with federal mine safety law.

This miner is working under: {mine_type}
"""

            try:
                print("📤 Sending request to OpenAI...")
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",  # change to "gpt-4" if you regain access
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_question}
                    ]
                )
                print("📥 Response received.")
                answer = response.choices[0].message.content
                st.success("Mr. Shaw says:")
                st.markdown(answer)
            except Exception as e:
                st.error(f"An error occurred while contacting OpenAI: {e}")
                print(f"❌ OpenAI Error: {e}")

# Disclaimer footer
st.markdown("""
---
**Disclaimer:** Mr. Shaw is an AI-powered assistant. While he draws on official MSHA CFR sources to provide guidance, 
his responses are not a substitute for formal training, legal advice, or direct MSHA consultation. 
Always verify compliance with a certified instructor or MSHA official.
""")
