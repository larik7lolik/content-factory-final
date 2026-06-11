#!/usr/bin/env python3
"""
Content Writer Agent for Content Factory
Creates platform-specific content based on research data
"""

import json
import os
import sys
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()
def create_content(topic, research_data):
    """
    Create platform-specific content based on research
    """
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    )

    platforms = [
        {"name": "Telegram", "audience": "подписчики Telegram канала", "format": "короткий пост с эмодзи и ключевыми моментами"},
        {"name": "VK", "audience": "ученики и родители в группе ВКонтакте", "format": "пост с заголовком, текстом и призывом к действию"},
        {"name": "Дзен", "audience": "читатели Яндекс Дзен", "format": "статья с заголовком, подзаголовками и списками"},
        {"name": "Блог", "audience": "посетители блога", "format": "подробная статья с примерами и практическими советами"},
        {"name": "TikTok", "audience": "молодежь в TikTok", "format": "сценарий с хэштегами и призывами взаимодействовать"}
    ]

    prompt = f"""
    На основе следующей информации создай контент для 5 платформ:

    Тема урока: {topic}

    Исследованная информация:
    {json.dumps(research_data, ensure_ascii=False, indent=2)}

    Для каждой платформы создай контент в соответствующем формате:
    """

    for i, platform in enumerate(platforms):
        prompt += f"{i+1}. {platform['name']} - для {platform['audience']}: {platform['format']}\n"

    prompt += """
    Верни ответ в формате JSON с полями для каждой платформы.
    Контент должен быть на русском языке.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": """Ты опытный контент-менеджер и копирайтер в сфере EdTech. Твоя задача - создавать привлекательный контент для различных платформ.

ОБЯЗАТЕЛЬНЫЕ ПРАВИЛА:
1. Верни ТОЛЬКО валидный JSON без markdown-обёрток (без ```json и ```)
2. JSON должен содержать следующие ключи: "Telegram", "VK", "Дзен", "Блог", "TikTok"
3. Контент должен быть на русском языке
4. Не добавляй никаких дополнительных пояснений или текста"""},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=2000
        )

        content_data = response.choices[0].message.content.strip()

        # More robust extraction of JSON content from markdown wrappers
        import re

        # Extract JSON from various markdown patterns
        json_match = re.search(r'```(?:json)?\s*({.*?})\s*```', content_data, re.DOTALL)
        if json_match:
            content_data = json_match.group(1)
        else:
            # If no markdown wrapper, try to find JSON object in the response
            json_start = content_data.find('{')
            json_end = content_data.rfind('}')
            if json_start != -1 and json_end != -1 and json_end > json_start:
                content_data = content_data[json_start:json_end+1]

        content_data = content_data.strip()

        # Try to parse as JSON
        try:
            parsed_json = json.loads(content_data)
            # Normalize key names to expected format
            normalized = {}
            key_mapping = {
                "telegram": "Telegram", "Telegram": "Telegram",
                "vk": "VK", "VK": "VK", "вконтакте": "VK", "ВКонтакте": "VK",
                "дзен": "Дзен", "Дзен": "Дзен", "yandex_zen": "Дзен", "Yandex_Dzen": "Дзен",
                "блог": "Блог", "Блог": "Блог", "blog": "Блог", "Blog": "Блог",
                "tiktok": "TikTok", "TikTok": "TikTok", "тикток": "TikTok"
            }

            for key, value in parsed_json.items():
                for norm_key, mapped_key in key_mapping.items():
                    if key.lower() == norm_key.lower():
                        normalized[mapped_key] = value
                        break
                else:
                    # If no mapping found, keep original key
                    normalized[key] = value

            return normalized
        except json.JSONDecodeError:
            return {"raw_content": content_data}

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python content_writer.py <topic> <research_file>")
        sys.exit(1)

    topic = sys.argv[1]

    # Read research data
    with open(sys.argv[2], "r", encoding="utf-8") as f:
        research_data = json.load(f)

    result = create_content(topic, research_data)

    # Save to file
    with open("content/platform_content.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(json.dumps(result, ensure_ascii=False, indent=2))