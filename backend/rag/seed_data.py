# Real scam patterns sourced from FTC and FBI IC3 reports
# These seed ChromaDB so Fraudar can find similar known scams

SCAM_PATTERNS = [
    {
        "id": "ftc_001",
        "text": "You have won a prize. Claim your gift card by providing your bank account details. Act now before the offer expires.",
        "metadata": {"type": "prize_scam", "source": "FTC", "risk": "high"}
    },
    {
        "id": "ftc_002",
        "text": "IRS notice: You owe back taxes. Pay immediately with gift cards or face arrest. Call this number now.",
        "metadata": {"type": "government_impersonation", "source": "FTC", "risk": "high"}
    },
    {
        "id": "ftc_003",
        "text": "Work from home opportunity. Earn $500 per day. No experience needed. Send $50 registration fee to get started.",
        "metadata": {"type": "job_scam", "source": "FTC", "risk": "high"}
    },
    {
        "id": "ftc_004",
        "text": "Your computer is infected with virus. Call Microsoft support immediately. Do not turn off your computer.",
        "metadata": {"type": "tech_support_scam", "source": "FTC", "risk": "high"}
    },
    {
        "id": "ftc_005",
        "text": "I am a foreign prince. I need your help transferring $10 million. You will receive 30% commission. Send your bank details.",
        "metadata": {"type": "advance_fee_fraud", "source": "FBI_IC3", "risk": "high"}
    },
    {
        "id": "ftc_006",
        "text": "Apartment for rent. Great location, low price. Send deposit via wire transfer before viewing. Owner is traveling abroad.",
        "metadata": {"type": "rental_scam", "source": "FBI_IC3", "risk": "high"}
    },
    {
        "id": "ftc_007",
        "text": "Your Amazon account has been compromised. Verify your identity by clicking this link and entering your password.",
        "metadata": {"type": "phishing", "source": "FTC", "risk": "high"}
    },
    {
        "id": "ftc_008",
        "text": "Investment opportunity in cryptocurrency. Guaranteed 200% returns in 30 days. Limited spots available. Invest now.",
        "metadata": {"type": "crypto_scam", "source": "FBI_IC3", "risk": "high"}
    },
    {
        "id": "ftc_009",
        "text": "I saw your profile online and fell in love. I am a military officer deployed overseas. I need money to come visit you.",
        "metadata": {"type": "romance_scam", "source": "FBI_IC3", "risk": "high"}
    },
    {
        "id": "ftc_010",
        "text": "Congratulations! You have been pre-approved for a loan. Pay processing fee of $200 to receive $10,000.",
        "metadata": {"type": "loan_scam", "source": "FTC", "risk": "high"}
    },
    {
        "id": "ftc_011",
        "text": "Job offer: Data entry position. Salary $800 per week. Send your social security number and bank details to apply.",
        "metadata": {"type": "job_scam", "source": "FTC", "risk": "high"}
    },
    {
        "id": "ftc_012",
        "text": "Your PayPal account is limited. Verify your information immediately or your account will be permanently suspended.",
        "metadata": {"type": "phishing", "source": "FTC", "risk": "high"}
    },
    {
        "id": "ftc_013",
        "text": "Student loan forgiveness program. Pay $500 processing fee to have all your student loans cancelled immediately.",
        "metadata": {"type": "debt_relief_scam", "source": "FTC", "risk": "high"}
    },
    {
        "id": "ftc_014",
        "text": "Buy our weight loss supplement. Lose 30 pounds in 30 days guaranteed. No diet or exercise needed. Order now.",
        "metadata": {"type": "fake_product_scam", "source": "FTC", "risk": "medium"}
    },
    {
        "id": "ftc_015",
        "text": "Social Security number suspended due to suspicious activity. Press 1 to speak with an officer or face arrest.",
        "metadata": {"type": "government_impersonation", "source": "FTC", "risk": "high"}
    }
]