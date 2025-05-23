# utils.py

def get_simulated_context(query):
    """
    Simple keyword-based simulated document retriever.
    Replace this with real MSHA document search in production.
    """
    docs = {
        "fall protection": {
            "snippet": "MSHA requires fall protection at elevations of 6 feet or more, per 30 CFR § 56.15005.",
            "citation": "30 CFR § 56.15005",
            "source": "https://www.ecfr.gov/current/title-30/part-56"
        },
        "first aid": {
            "snippet": "First aid materials must be readily accessible in every mine. See 30 CFR § 56.18010.",
            "citation": "30 CFR § 56.18010",
            "source": "https://www.ecfr.gov/current/title-30/part-56"
        },
        "task training": {
            "snippet": "30 CFR § 46.7 requires task training before miners perform new tasks that pose health/safety risks.",
            "citation": "30 CFR § 46.7",
            "source": "https://www.ecfr.gov/current/title-30/part-46"
        }
    }

    # Simple keyword match
    for keyword, data in docs.items():
        if keyword in query.lower():
            return data
    return None

def format_response(ai_text, doc):
    """
    Combine AI output with citation details if available.
    """
    result = f"👷 **Mr. Shaw Says:**\n\n{ai_text.strip()}\n"

    if doc:
        result += f"\n📘 **Rule Cited:** {doc['citation']}  \n🔗 [View Rule]({doc['source']})"
    return result
