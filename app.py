import streamlit as st
from openai import OpenAI

# Debug: confirm OpenAI client initialization
try:
    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"],
        organization=st.secrets.get("OPENAI_ORG_ID", None),
        project=st.secrets.get("OPENAI_PROJECT_ID", None)
    )
    print("✅ OpenAI client initialized.")
except Exception as init_error:
    st.error(f"❌ Failed to initialize OpenAI client: {init_error}")
    print(f"❌ OpenAI Init Error: {init_error}")

# UI layout
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

# Button trigger
if st.button("Ask Mr. Shaw"):
    if not user_question or user_question.strip() == "":
        st.warning("Please type a question before submitting.")
    else:
        print("✅ Button clicked. User question:", user_question)
        with st.spinner("Mr. Shaw is reviewing the CFR..."):
            system_prompt = f"""
You are Mr. Shaw, a certified MSHA instructor with over 30 years of experience. When a miner asks a safety question,
you respond as a structured MSHA instructor—not a chatbot. Provide clear, CFR-based training guidance.

Use this format:
------------------------------
🟦 **Module Title: [Insert Topic]**

### 📍 What to Do or Where to File
- Bullet points with clear actions
- Emphasize key steps
- Include real links like [MSHA.gov](https://www.msha.gov)

### 📝 Information Needed
- List specific steps or documentation
- Explain what's required and why

📘 **CFR Reference**: Include the exact 30 CFR or Mine Act citation

------------------------------

Only use MSHA regulations. Do not reference OSHA. No generalizations. Base everything strictly on 30 CFR.

This miner is working under: {mine_type}
"""

            try:
                print("📤 Sending to OpenAI...")
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",  # safest model for now
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_question}
                    ]
                )
                print("📥 OpenAI responded.")
                answer = response.choices[0].message.content
                st.success("Mr. Shaw says:")
                st.markdown(answer)
            except Exception as e:
                st.error(f"❌ OpenAI request failed: {e}")
                print(f"❌ OpenAI Error: {e}")

# Footer disclaimer
st.markdown("""
---
**Disclaimer:** Mr. Shaw is an AI-powered assistant. While he draws on official MSHA CFR sources to provide guidance, 
his responses are not a substitute for formal training, legal advice, or direct MSHA consultation. 
Always verify compliance with a certified instructor or MSHA official.
""")
