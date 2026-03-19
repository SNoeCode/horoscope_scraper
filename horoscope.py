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

    MOODS = [
        'cautious and introspective', 'bold and decisive', 'warm and romantic',
        'grounded and practical', 'restless and curious', 'hopeful and optimistic',
        'reflective and healing', 'sharp and ambitious', 'playful and light',
        'serious and determined', 'tender and vulnerable', 'energized and confident'
    ]

    FOCUS_AREAS = ['love', 'career', 'finances', 'health', 'personal growth']

    def __init__(self):
        self.token = os.environ.get('GROQ_API_KEY', '')
        self.headers = {
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'application/json'
        }

    def _pick(self, pool, seed):
        index = int(hashlib.md5(seed.encode()).hexdigest(), 16) % len(pool)
        return pool[index]

    def generate_horoscope(self, sign):
        if sign not in self.SIGNS:
            print("Invalid sign: " + sign)
            return None

        today = datetime.now().strftime('%B %d, %Y')
        traits = self.SIGN_TRAITS.get(sign, '')

        # Each sign gets its own theme and mood, independent of other signs
        theme = self._pick(self.THEMES, today + sign)
        mood = self._pick(self.MOODS, sign + today)
        focus = self._pick(self.FOCUS_AREAS, sign + today + 'focus')

        payload = {
            'model': self.MODEL,
            'messages': [
                {
                    'role': 'system',
                    'content': (
                        'You are an astrologer writing sharp, varied daily horoscopes. '
                        'Each sign must read completely differently — different structure, different vocabulary, different emotional register. '
                        'Some horoscopes are a warning. Some are an invitation. Some are a push. Some are reassurance. '
                        'Avoid generic spiritual filler. Be concrete: name a situation, a tension, a choice, or an opportunity. '
                        'Never start two horoscopes the same way.'
                    )
                },
                {
                    'role': 'user',
                    'content': (
                        f'Write a daily horoscope for {sign.capitalize()} for {today}.\n'
                        f'Sign traits: {traits}.\n'
                        f"Today's theme: {theme}.\n"
                        f'Tone: {mood}.\n'
                        f'Focus area: {focus} only — do not cover other areas.\n'
                        f'3–4 sentences. Name a specific action, decision, or situation — not just a feeling. '
                        f'Do not use the phrases "inner wisdom", "inner voice", "the universe", or "tap into". '
                        f'Return only the horoscope paragraph.'
                    )
                }
            ],
            'max_tokens': 250,
            'temperature': 0.95
        }

        try:
            response = requests.post(self.API_URL, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            text = result['choices'][0]['message']['content'].strip()

            time.sleep(1)

            return {
                'date': today,
                'summary': text,
                'scraped_at': datetime.now().isoformat()
            }

        except requests.RequestException as e:
            print("Error generating horoscope for " + sign + ": " + str(e))
            return None
