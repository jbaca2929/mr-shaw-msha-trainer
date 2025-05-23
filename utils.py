def get_simulated_context(query):
    data = {
        "fall protection": {
            "snippet": "MSHA requires fall protection at elevations of 6 feet or more (30 CFR § 56.15005).",
            "citation": "30 CFR § 56.15005",
            "source": "https://www.ecfr.gov/current/title-30/part-56"
        },
        "first aid": {
            "snippet": "Mines must have accessible first aid supplies per 30 CFR § 56.18010.",
            "citation": "30 CFR § 56.18010",
            "source": "https://www.ecfr.gov/current/title-30/part-56"
        },
        "task training": {
            "snippet": "30 CFR § 46.7 requires task training when assigning miners new tasks.",
            "citation": "30 CFR § 46.7",
            "source": "https://www.ecfr.gov/current/title-30/part-46"
        }
    }
    for keyword, doc in data.items():
        if keyword in query.lower():
            return doc
    return None

def format_response(text, doc):
    formatted = f"👷 **Mr. Shaw Says:**\n\n{text}\n"
    if doc:
        formatted += f"\n📘 **Rule Cited:** {doc['citation']}  \n🔗 [View Rule]({doc['source']})"
    return formatted
