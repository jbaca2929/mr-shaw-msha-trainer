import streamlit as st
from datetime import datetime
from openai import OpenAI

# Init
st.set_page_config(page_title="Mr. Shaw MSHA Trainer", layout="centered")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("👷‍♂️ Mr. Shaw MSHA Trainer")
st.markdown("**MSHA-compliant safety guidance from a certified instructor—just ask.**")

# --- Mine Type Selector ---
mine_type = st.radio("🛠️ What type of mine are you working on?", 
    ["Part 46 – Sand & Gravel", "Part 48 – Surface Mine", "Part 48 – Underground Mine"])

# --- Topic Tags (Optional Presets) ---
st.markdown("### 🧭 Choose a topic or ask your own question:")
cols = st.columns(5)
topics = ["Equipment Safety", "Emergency", "Handling", "HazCom", "Fall Prot."]
for i, topic in enumerate(topics):
    with cols[i]:
        st.button(f"📌 {topic}", key=f"tag_{i}")

# --- User Input ---
st.markdown("### ✏️ What’s your safety question today?")
user_question = st.text_input("Type your question below:", placeholder="e.g., When is fall protection required on a loader ramp?")
st.button("🎤 Speak (voice input coming soon)", disabled=True)

# --- Simulated RAG Lookup ---
def simulated_doc_search(query):
    examples = {
        "fall protection": {
            "snippet": "MSHA requires fall protection where there is a danger of falling more than 6 feet, per 30 CFR § 56.15005.",
            "citation": "30 CFR § 56.15005",
            "source": "https://www.ecfr.gov/current/title-30/part-56"
        },
        "first aid": {
            "snippet": "First aid materials must be readily available at all mines. Part 46 requires compliance with 30 CFR § 56.18010.",
            "citation": "30 CFR § 56.18010",
            "source": "https://www.ecfr.gov/current/title-30/part-56"
        },
        "task training": {
            "snippet": "New miners and experienced miners assigned new tasks must receive task training under 30 CFR § 46.7.",
            "citation": "30 CFR § 46.7",
            "source": "https://www.ecfr.gov/current/title-30/part-46"
        }
    }
    for keyword, data in examples.items():
        if keyword in query.lower():
            return data
    return None

# --- Ask Mr. Shaw ---
if st.button("🔵 Ask Mr. Shaw") and user_question:
    with st.spinner("Mr. Shaw is reviewing the CFR..."):

        # RAG-like grounding
        doc = simulated_doc_search(user_question)
        context = doc["snippet"] if doc else "No document match found. Mr. Shaw will answer using general MSHA rules."

        # Compose prompt
        system_prompt = f"""
You are Mr. Shaw, a certified MSHA instructor with 30+ years of field experience. Speak directly and cite only official MSHA, CFR, or NIOSH rules.

Your tone is instructional, experienced, and confident. You always:
- Summarize in plain language
- Quote the regulation and explain what it means
- Provide a citation like 30 CFR § 46.5
- Keep it under 300 words unless asked for more detail

Mine Type: {mine_type}
Context from MSHA documents: {context}
"""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ],
            temperature=0.3
        )

        full_reply = response.choices[0].message.content.strip()

        # --- Display Answer ---
        st.divider()
        st.subheader("👷 Mr. Shaw Says:")
        st.markdown(full_reply)

        if doc:
            st.markdown(f"📘 **Rule Cited:** {doc['citation']}")
            st.markdown(f"🔗 [View Rule]({doc['source']})")

        cols = st.columns(2)
        with cols[0]:
            st.button("⭐ Save this lesson")
        with cols[1]:
            st.button("📄 Export to PDF", disabled=True)

        st.warning("⚠️ Always follow your site-specific safety plan and confirm with your certified trainer.")

# --- Footer ---
st.caption(f"App version 0.2 — Generated on {datetime.now().strftime('%B %d, %Y')}")
