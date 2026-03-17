#!/usr/bin/env python3
"""
Generates daily horoscopes for all zodiac signs using HuggingFace
and saves to horoscope.json
"""

import json
import os
from horoscope import HoroscopeGenerator


def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("  [OK] Saved " + path)


def main():
    print("=" * 60)
    print("Generating Daily Horoscopes with HuggingFace")
    print("=" * 60)

    generator = HoroscopeGenerator()
    combined = {}

    for sign in generator.SIGNS:
        print("\nGenerating " + sign.upper() + "...")
        daily = generator.generate_horoscope(sign)
        if daily:
            combined[sign] = daily

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'horoscope.json')
    save_json(output_path, combined)
    print("\nDone! Generated " + str(len(combined)) + " signs.")


if __name__ == "__main__":
    main()
