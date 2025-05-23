import streamlit as st
from openai import OpenAI

# Page settings
st.set_page_config(page_title="Mr. Shaw MSHA Trainer – GPT-4 Test", layout="centered")
st.title("👷‍♂️ Mr. Shaw MSHA Trainer")
st.markdown("**🧪 Testing GPT-4 connection with OpenAI**")

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Trigger button
if st.button("🔵 Test GPT-4 Connection"):
    with st.spinner("Calling GPT-4 as Mr. Shaw..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": "Say hello as Mr. Shaw would at a safety meeting."}
                ]
            )

            ai_output = response.choices[0].message.content.strip()
            st.success("✅ GPT-4 responded successfully:")
            st.markdown(ai_output)

        except Exception as e:
            st.error("❌ GPT-4 API call failed. Check your API key, access, or usage limits.")
            st.code(str(e))
