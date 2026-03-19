"""
Groq Daily Horoscope Generator
Generates daily horoscopes for all zodiac signs using the Groq free API
"""

import requests
import os
import hashlib
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

    THEMES = [
        'communication and clarity', 'rest and reflection', 'bold action and risk-taking',
        'finances and practical decisions', 'relationships and emotional depth',
        'creativity and self-expression', 'ambition and career focus',
        'healing and letting go', 'new beginnings and fresh starts',
        'patience and steady progress', 'intuition and inner wisdom',
        'social connections and community'
    ]

    def __init__(self):
        self.token = os.environ.get('GROQ_API_KEY', '')
        self.headers = {
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'application/json'
        }

    def _daily_theme(self, date_str):
        index = int(hashlib.md5(date_str.encode()).hexdigest(), 16) % len(self.THEMES)
        return self.THEMES[index]

    def generate_horoscope(self, sign):
        if sign not in self.SIGNS:
            print("Invalid sign: " + sign)
            return None

        today = datetime.now().strftime('%B %d, %Y')
        traits = self.SIGN_TRAITS.get(sign, '')
        theme = self._daily_theme(today)

        payload = {
            'model': self.MODEL,
            'messages': [
                {
                    'role': 'system',
                    'content': (
                        'You are an astrologer writing daily horoscopes. '
                        'Each day must feel meaningfully different — vary the tone, focus, and specific advice. '
                        'Never reuse phrases from previous days. '
                        'Some days are challenging, some are lucky, some are introspective — mix it up.'
                    )
                },
                {
                    'role': 'user',
                    'content': (
                        'Write a daily horoscope for ' + sign.capitalize() + ' for ' + today + '. '
                        + sign.capitalize() + ' is ' + traits + '. '
                        "Today's energy: " + theme + '. '
                        'Write 3-4 sentences. Cover one or two areas from: love, career, finances, health, or personal growth — not all of them every day. '
                        'Vary the mood — sometimes cautious, sometimes bold, sometimes reflective. '
                        'Be specific and direct. Return only the horoscope paragraph, no headings or labels.'
                    )
                }
            ],
            'max_tokens': 200,
            'temperature': 0.95
        }

        try:
            response = requests.post(self.API_URL, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            text = result['choices'][0]['message']['content'].strip()

            time.sleep(1)

            return {
                'date': datetime.now().strftime('%B %d, %Y'),
                'summary': text,
                'scraped_at': datetime.now().isoformat()
            }

        except requests.RequestException as e:
            print("Error generating horoscope for " + sign + ": " + str(e))
            return None
