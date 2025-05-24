import streamlit as st
import openai
import json

# OpenAI API Key (set from Streamlit secrets)
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit Page Setup
st.set_page_config(page_title="Mr. Shaw – Your MSHA Trainer")
st.title("👷 Mr. Shaw – Your MSHA Trainer")
st.markdown("Ask an MSHA safety question and Mr. Shaw will answer based on official CFR guidance.")

# Mine Type Selection
mine_type = st.radio(
    "Select your mine type:",
    ["Part 46 – Sand & Gravel", "Part 48 – Surface Mine", "Part 48 – Underground Mine"]
)

# User Question Input
user_question = st.text_input("Type your MSHA safety question:")

# Action Button
if st.button("Ask Mr. Shaw"):
    if not user_question.strip():
        st.warning("Please type a question before submitting.")
    else:
        st.info("Mr. Shaw is reviewing the CFR...")

        # CFR Scope Enforcement
        if "Part 46" in mine_type:
            allowed_cfr = "Only cite regulations from 30 CFR Part 46. Do not include references to Part 48 or Part 56."
        elif "Underground" in mine_type:
            allowed_cfr = "Only cite regulations from 30 CFR Part 48 Subpart A. Do not include references to Part 46 or Part 56."
        else:
            allowed_cfr = "Only cite regulations from 30 CFR Part 48 Subpart B. Do not include references to Part 46 or Part 56."

        # Build Prompt
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

        # Make API Call
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_question}
                ]
            )

            # Extract Response
            result = response["choices"][0]["message"]["content"].strip()
            st.success("Mr. Shaw says:")
            st.markdown(result)

            # Optional Debug Log
            print("✅ OpenAI response:", json.dumps(response, indent=2))

        except Exception as e:
            st.error("OpenAI request failed. Please check your API key, model access, or try again later.")
            print("❌ OpenAI API error:", str(e))

# Footer Disclaimer
st.markdown("""
---
**Disclaimer:** Mr. Shaw is an AI-powered assistant. While he draws on official MSHA CFR sources to provide guidance, 
his responses are not a substitute for formal training, legal advice, or direct MSHA consultation. 
Always verify compliance with a certified instructor or MSHA official.
""")
