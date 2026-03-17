"""
Groq Daily Horoscope Generator
Generates daily horoscopes for all zodiac signs using the Groq free API
"""

import requests
import os
from datetime import datetime
import time


class HoroscopeGenerator:

    API_URL = "https://api.groq.com/openai/v1/chat/completions"
    MODEL = "llama-3.3-70b-versatile"

    SIGNS = [
        'aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo',
        'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces'
    ]

    SIGN_TRAITS = {
        'aries': 'bold, energetic, and pioneering',
        'taurus': 'grounded, patient, and determined',
        'gemini': 'curious, adaptable, and communicative',
        'cancer': 'intuitive, nurturing, and emotional',
        'leo': 'confident, creative, and generous',
        'virgo': 'analytical, practical, and detail-oriented',
        'libra': 'balanced, diplomatic, and charming',
        'scorpio': 'intense, passionate, and transformative',
        'sagittarius': 'adventurous, optimistic, and philosophical',
        'capricorn': 'ambitious, disciplined, and persistent',
        'aquarius': 'innovative, independent, and humanitarian',
        'pisces': 'dreamy, empathetic, and artistic'
    }

    def __init__(self):
        self.token = os.environ.get('GROQ_API_KEY', '')
        self.headers = {
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'application/json'
        }

    def generate_horoscope(self, sign):
        if sign not in self.SIGNS:
            print("Invalid sign: " + sign)
            return None

        today = datetime.now().strftime('%B %d, %Y')
        traits = self.SIGN_TRAITS.get(sign, '')

        payload = {
            'model': self.MODEL,
            'messages': [
                {
                    'role': 'user',
                    'content': (
                        'Write a daily horoscope for ' + sign.capitalize() + ' for ' + today + '. '
                        + sign.capitalize() + ' is ' + traits + '. '
                        'Write 3-4 sentences in a friendly, straightforward tone. '
                        'Give practical, grounded advice covering love, career, and personal growth. '
                        'Avoid overly poetic or mystical language. '
                        'Return only the horoscope paragraph, no headings or labels.'
                    )
                }
            ],
            'max_tokens': 200,
            'temperature': 0.85
        }

        try:
            response = requests.post(self.API_URL, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            text = result['choices'][0]['message']['content'].strip()

            # wait 1 second between calls to stay within rate limits
            time.sleep(1)

            return {
                'date': datetime.now().strftime('%B %d, %Y'),
                'summary': text,
                'scraped_at': datetime.now().isoformat()
            }

        except requests.RequestException as e:
            print("Error generating horoscope for " + sign + ": " + str(e))
            return None
