import streamlit as st
from openai import OpenAI

# Set config FIRST
st.set_page_config(page_title="Mr. Shaw – MSHA Trainer")

# Initialize OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def main():
    st.title("👷 Mr. Shaw – MSHA Trainer")
    st.write("MSHA-compliant safety guidance from a certified instructor—just ask.")

    # Input fields
    mine_type = st.radio("🔧 What type of mine are you working on?", [
        "Part 46 – Sand & Gravel",
        "Part 48 – Surface Mine",
        "Part 48 – Underground Mine"
    ])

    user_question = st.text_input("Type your MSHA safety question:")
    submit = st.button("🔵 Ask Mr. Shaw")

    # Debug block
    st.markdown("### 🪪 Debug info:")
    st.write("Mine type:", mine_type)
    st.write("Question entered:", user_question)
    st.write("Submit clicked:", submit)

    if submit and user_question:
        with st.spinner("Mr. Shaw is reviewing the CFR..."):
            system_prompt = f"""
You are Mr. Shaw, a certified MSHA instructor with 30+ years of field experience.
Speak like you're training real miners—direct, practical, and legally correct.

- Summarize in plain terms
- Quote the regulation when relevant
- Always cite MSHA/NIOSH/CFR officially (e.g., 30 CFR § 56.15005)
- Mine Type: {mine_type}
- Question: {user_question}
"""

            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_question}
                    ],
                    temperature=0.3
                )
                answer = response.choices[0].message.content.strip()
                st.success("✅ Mr. Shaw responded:")
                st.write(answer)
            except Exception as e:
                st.error("❌ GPT error:")
                st.code(str(e))

# Required: call main()
if __name__ == "__main__":
    main()
