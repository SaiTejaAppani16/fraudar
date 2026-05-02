import requests
from bs4 import BeautifulSoup
from anthropic import Anthropic
from backend.config import ANTHROPIC_API_KEY

client = Anthropic(api_key=ANTHROPIC_API_KEY)

def scrape_url_content(url: str) -> str:
    """
    Visits a URL and extracts all readable text from the page.
    Used to get content for analysis without the user having to copy paste.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Remove script and style tags — we only want visible text
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        
        text = soup.get_text(separator=" ", strip=True)
        
        # Limit to 3000 characters to stay within Claude token limits
        return text[:3000]
    
    except Exception as e:
        return f"Error scraping URL: {str(e)}"


def analyze_text_for_scams(text: str) -> dict:
    """
    Sends extracted text to Claude for scam pattern analysis.
    """
    prompt = f"""You are a scam detection expert. Analyze the following text and determine if it contains scam indicators.

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

    import json
    response_text = message.content[0].text.strip()
    
    # Strip markdown code blocks if Claude adds them
    if response_text.startswith("```"):
        response_text = response_text.split("```")[1]
        if response_text.startswith("json"):
            response_text = response_text[4:]
    
    return json.loads(response_text.strip())


async def analyze_content(text: str = None, url: str = None) -> dict:
    """
    Master function — accepts either raw text or a URL.
    If URL is provided, scrapes it first then analyzes the content.
    """
    if url and not text:
        text = scrape_url_content(url)
    
    if not text:
        return {"error": "No text or URL provided"}
    
    analysis = analyze_text_for_scams(text)
    
    return {
        "source": url if url else "direct_text",
        "content_preview": text[:200] + "..." if len(text) > 200 else text,
        "analysis": analysis
    }