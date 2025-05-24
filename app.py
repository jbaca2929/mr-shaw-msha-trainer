import streamlit as st
from openai import OpenAI

# Set up Streamlit page
st.set_page_config(page_title="Mr. Shaw – MSHA Trainer")
st.title("👷 Mr. Shaw – MSHA Trainer")
st.markdown("MSHA-compliant safety guidance from a certified instructor—just ask.")

# Get API key securely
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Mine type selection
mine_type = st.radio(
    "🛠️ What type of mine are you working on?",
    ["Part 46 – Sand & Gravel", "Part 48 – Surface Mine", "Part 48 – Underground Mine"],
)

# Question input
user_question = st.text_input("Type your MSHA safety question:")

# Submit button and result logic
submit = st.button("🔵 Ask Mr. Shaw")

if submit and user_question.strip():
    with st.spinner("Mr. Shaw is reviewing the CFR..."):
        try:
            system_prompt = f"""
You are Mr. Shaw, a certified MSHA instructor with 30+ years of field experience.
Speak like you're training real miners—direct, practical, and legally correct.
Only cite MSHA or CFR. The miner is working under: {mine_type}.
            """

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt.strip()},
                    {"role": "user", "content": user_question.strip()}
                ],
                temperature=0.4
            )

            result = response.choices[0].message.content
            st.success("✅ Mr. Shaw says:")
            st.markdown(result)

        except Exception as e:
            st.error(f"❌ Something went wrong: {e}")
elif submit:
    st.warning("Please enter a safety question before asking.")
