import streamlit as st
from openai import OpenAI

# Basic config
st.set_page_config(page_title="Mr. Shaw – Your MSHA Trainer")
st.title("👷 Mr. Shaw – Your MSHA Trainer")
st.markdown("Ask an MSHA safety question and Mr. Shaw will answer based on official CFR guidance.")

# Mine type
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

# Ask button
if st.button("Ask Mr. Shaw"):
    if not user_question.strip():
        st.warning("Please type a question before submitting.")
    else:
        st.info("Mr. Shaw is reviewing the CFR...")

        # Connect to OpenAI
        try:
            client = OpenAI(
                api_key=st.secrets["OPENAI_API_KEY"],
                organization=st.secrets.get("OPENAI_ORG_ID", None),
                project=st.secrets.get("OPENAI_PROJECT_ID", None)
            )
            print("✅ OpenAI client loaded.")
        except Exception as e:
            st.error(f"Failed to initialize OpenAI: {e}")
            print(f"❌ OpenAI Init Error: {e}")
            st.stop()

        # Construct system prompt
        system_prompt = f"""
You are Mr. Shaw, a certified MSHA instructor with 30+ years of field experience. Answer the following safety question
in the format of a structured CFR-compliant training module—not a chatbot. Use official MSHA guidance only.

Use this format:
------------------------------
🟦 **Module Title: [Insert Topic]**

### 📍 What to Do or Where to File
- Bullet list of clear steps
- Link to [MSHA.gov](https://www.msha.gov) if applicable

### 📝 Information Needed
- Bullet list of specific documentation, evidence, or info to gather

📘 **CFR Reference**: Cite the specific CFR section or Mine Act section

------------------------------
The miner is working under: {mine_type}
Only use 30 CFR regulations. Do not mention OSHA or general rules.
"""

        try:
            # API call
            print("📤 Sending question to OpenAI...")
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_question}
                ]
            )
            result = response.choices[0].message.content
            print("📥 Response received.")
            st.success("Mr. Shaw says:")
            st.markdown(result)

        except Exception as e:
            st.error(f"An error occurred: {e}")
            print(f"❌ OpenAI Request Error: {e}")
