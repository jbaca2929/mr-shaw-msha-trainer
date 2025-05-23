import gradio as gr
from openai import OpenAI

# Initialize OpenAI
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

def ask_mr_shaw(mine_type, user_question):
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
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# Gradio UI components
radio = gr.Radio(choices=["Part 46 – Sand & Gravel", "Part 48 – Surface Mine", "Part 48 – Underground Mine"], label="What type of mine are you working on?")
textbox = gr.Textbox(lines=2, placeholder="e.g., What are the rules for fall protection?", label="Your MSHA safety question")
output = gr.Textbox(label="Mr. Shaw's Response")

demo = gr.Interface(fn=ask_mr_shaw, inputs=[radio, textbox], outputs=output, title="👷 Mr. Shaw – MSHA Trainer")

# Launch the app
demo.launch()
