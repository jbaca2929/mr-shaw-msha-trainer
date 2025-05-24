import streamlit as st
from openai import OpenAI

# Streamlit layout
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

# Button
if st.button("Ask Mr. Shaw"):
    print("🟢 Button clicked")
    if not user_question.strip():
        st.warning("Please type a question before submitting.")
        print("⚠️ No question entered.")
    else:
        print(f"✅ Received question: {user_question}")
        st.info("Mr. Shaw is reviewing the CFR...")

        # OpenAI client
        try:
            client = OpenAI(
                api_key=st.secrets["OPENAI_API_KEY"],
                organization=st.secrets.get("OPENAI_ORG_ID", None),
                project=st.secrets.get("OPENAI_PROJECT_ID", None)
            )
            print("✅ OpenAI client initialized.")
        except Exception as e:
            st.error(f"OpenAI client error: {e}")
            print(f"❌ Client init error: {e}")
            st.stop()

        # CFR scope
        if "Part 46" in mine_type:
            allowed_cfr = "Only cite regulations from 30 CFR Part 46. Do not include references to Part 48 or Part 56."
        elif "Underground" in mine_type:
            allowed_cfr = "Only cite regulations from 30 CFR Part 48 Subpart A. Do not include references to Part 46 or Part 56."
        else:
            allowed_cfr = "Only cite regulations from 30 CFR Part 48 Subpart B. Do not include references to Part 46 or Part 56."

        # Prompt
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
The miner is working under: {mine_type}.
{allowed_cfr}
"""

        # API call
        try:
            print("📤 Calling OpenAI API...")
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # safest model for compatibility
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_question}
                ]
            )
            print("📥 Response received.")
            result = response.choices[0].message.content
            st.success("Mr. Shaw says:")
            st.markdown(result)
        except Exception as e:
            st.error(f"OpenAI request failed: {e}")
            print(f"❌ API error: {e}")
