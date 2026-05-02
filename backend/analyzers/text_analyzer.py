import requests
from bs4 import BeautifulSoup
from anthropic import Anthropic
from backend.config import ANTHROPIC_API_KEY
from backend.rag.rag_pipeline import search_similar_scams
import json

client = Anthropic(api_key=ANTHROPIC_API_KEY)

def scrape_url_content(url: str) -> str:
    """
    Visits a URL and extracts all readable text from the page.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        return text[:3000]

    except Exception as e:
        return f"Error scraping URL: {str(e)}"


def analyze_text_for_scams(text: str) -> dict:
    """
    Sends extracted text to Claude with RAG context for scam analysis.
    """
    # Step 1 — Search ChromaDB for similar known scams
    similar_scams = search_similar_scams(text, n_results=3)

    # Step 2 — Format RAG context for Claude
    rag_context = ""
    if similar_scams:
        rag_context = "Known scam patterns similar to this submission:\n"
        for i, scam in enumerate(similar_scams, 1):
            rag_context += f"{i}. Type: {scam['scam_type']} | Source: {scam['source']} | Similarity: {scam['similarity_score']}\n"
            rag_context += f"   Pattern: {scam['pattern']}\n"

    # Step 3 — Send to Claude with RAG context included
    prompt = f"""You are a scam detection expert. Analyze the following text and determine if it contains scam indicators.

{rag_context}

Text to analyze:
{text}

Respond in this exact JSON format with no extra text, no markdown, no backticks:
{{
    "scam_probability": <integer 0-100>,
    "scam_type": "<phishing|job_scam|rental_scam|romance_scam|crypto_scam|fake_store|legitimate|unknown>",
    "red_flags": ["<flag1>", "<flag2>", "<flag3>"],
    "explanation": "<2-3 sentence plain English explanation>",
    "recommended_action": "<ignore|proceed_with_caution|avoid|report_to_ftc>"
}}"""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = message.content[0].text.strip()

    if response_text.startswith("```"):
        response_text = response_text.split("```")[1]
        if response_text.startswith("json"):
            response_text = response_text[4:]

    return json.loads(response_text.strip())


async def analyze_content(text: str = None, url: str = None) -> dict:
    """
    Master function — accepts either raw text or a URL.
    """
    if url and not text:
        text = scrape_url_content(url)

    if not text:
        return {"error": "No text or URL provided"}

    analysis = analyze_text_for_scams(text)
    similar_scams = search_similar_scams(text, n_results=3)

    return {
        "source": url if url else "direct_text",
        "content_preview": text[:200] + "..." if len(text) > 200 else text,
        "similar_known_scams": similar_scams,
        "analysis": analysis
    }