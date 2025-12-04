import requests
from bs4 import BeautifulSoup
import re

# ----- Tools -----

def fetch_page(url):
    return requests.get(url).text

def clean_html(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_sentences(text):
    return re.split(r'\.|\n', text)

LEGAL_TOPICS = {
    "Data Collection": ["data", "collect", "information", "personal"],
    "Privacy": ["privacy", "store", "protect"],
    "Third Party Sharing": ["third", "partners", "share", "external"],
    "Payments": ["payment", "billing", "subscription", "purchase"],
    "Cancellation": ["cancel", "terminate", "end", "stop"],
    "Refunds": ["refund", "return", "money"],
    "Liability": ["liable", "responsible", "risk", "damage"],
    "User Responsibilities": ["responsible", "must", "agree", "require"]
}

# ----- Extract Summary -----

def generate_summary(text):
    sentences = extract_sentences(text)
    important = [
        s for s in sentences
        if any(k in s.lower() for k in ["data", "privacy", "responsible", "terms"])
    ]
    return " ".join(important[:4])

# ----- Extract Key Points -----

def extract_key_points(text):
    sentences = extract_sentences(text)
    points = []

    for topic, keywords in LEGAL_TOPICS.items():
        for s in sentences:
            if any(k.lower() in s.lower() for k in keywords):
                points.append(f"{topic}: {s.strip()}")
                break
    return points

# ----- Main Agent -----

def terms_agent(url):
    html = fetch_page(url)
    text = clean_html(html)

    summary = generate_summary(text)
    key_points = extract_key_points(text)

    return {
        "summary": summary,
        "key_points": key_points
    }

# Example usage
if __name__ == "__main__":
    url = "https://policies.google.com/terms"
    output = terms_agent(url)
    print("SUMMARY:\n", output["summary"])
    print("\nKEY POINTS:")
    for kp in output["key_points"]:
        print("-", kp)
