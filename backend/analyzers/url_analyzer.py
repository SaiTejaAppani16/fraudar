import httpx
from backend.config import VIRUSTOTAL_API_KEY, GOOGLE_SAFE_BROWSING_API_KEY
import base64

async def check_virustotal(url: str) -> dict:
    """
    Submits URL to VirusTotal and returns analysis results.
    VirusTotal checks the URL against 70+ antivirus engines.
    """
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    
    # VirusTotal requires URL to be base64 encoded
    url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://www.virustotal.com/api/v3/urls/{url_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            stats = data["data"]["attributes"]["last_analysis_stats"]
            return {
                "malicious": stats.get("malicious", 0),
                "suspicious": stats.get("suspicious", 0),
                "harmless": stats.get("harmless", 0),
                "undetected": stats.get("undetected", 0)
            }
        else:
            return {"error": "VirusTotal analysis failed", "status_code": response.status_code}


async def check_google_safe_browsing(url: str) -> dict:
    """
    Checks URL against Google Safe Browsing database.
    Google maintains a list of known phishing and malware URLs.
    """
    api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={GOOGLE_SAFE_BROWSING_API_KEY}"
    
    payload = {
        "client": {
            "clientId": "fraudar",
            "clientVersion": "1.0.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(api_url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            threats = data.get("matches", [])
            return {
                "is_threat": len(threats) > 0,
                "threats": [t.get("threatType") for t in threats]
            }
        else:
            return {"error": "Google Safe Browsing check failed", "status_code": response.status_code}


async def analyze_url(url: str) -> dict:
    """
    Master function that runs all URL checks and returns combined result.
    """
    vt_result = await check_virustotal(url)
    gsb_result = await check_google_safe_browsing(url)
    
    # Calculate risk score based on results
    risk_score = 0
    
    if "malicious" in vt_result:
        malicious = vt_result["malicious"]
        suspicious = vt_result["suspicious"]
        risk_score += min((malicious * 10) + (suspicious * 5), 60)
    
    if gsb_result.get("is_threat"):
        risk_score += 40
    
    risk_score = min(risk_score, 100)
    
    return {
        "url": url,
        "risk_score": risk_score,
        "virustotal": vt_result,
        "google_safe_browsing": gsb_result,
        "verdict": "dangerous" if risk_score >= 70 else "suspicious" if risk_score >= 40 else "safe"
    }