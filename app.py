import streamlit as st
from openai import OpenAI

# Set page config
st.set_page_config(page_title="Mr. Shaw – MSHA Trainer")

# Initialize OpenAI client using Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# UI Layout
st.title("👷 Mr. Shaw – MSHA Trainer")
st.caption("MSHA-compliant safety guidance from a certified instructor—just ask.")

mine_type = st.radio(
    "🛠️ What type of mine are you working on?",
    ["Part 46 – Sand & Gravel", "Part 48 – Surface Mine", "Part 48 – Underground Mine"]
)

user_question = st.text_input("Type your MSHA safety question:")
submit = st.button("🔵 Ask Mr. Shaw")

if submit and user_question:
    with st.spinner("Mr. Shaw is reviewing the CFR..."):
        system_prompt = f"""
        You are Mr. Shaw, a certified MSHA instructor with 30+ years of field experience.
        Respond with clear, legally accurate guidance based on current MSHA standards.
        Assume the miner is working in: {mine_type}.
        Speak like you're training real miners—direct, practical, and legally correct.
        Include the relevant CFR citation (e.g., 30 CFR § 56.15005) when applicable.
        """

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ]
        )

        answer = response.choices[0].message.content
        st.success("✅ Response from Mr. Shaw:")
        st.markdown(answer)
