#!/usr/bin/env python3
"""
Researcher Agent for Content Factory
Responsible for gathering relevant information about a given lesson topic
"""

import json
import os
import sys
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()
def research_topic(topic):
    """
    Research a topic and return relevant information
    """
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    )

    prompt = f"""
    Исследуй тему урока: "{topic}"

    Верни структурированную информацию, включая:
    - Ключевые понятия темы
    - Основные факты и данные
    - Интересные примеры или кейсы
    - Возможные подтемы или расширения

    Ответ должен быть на русском языке и представлен в формате JSON.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты эксперт в области образования и маркетинга. Твоя задача - исследовать тему урока и предоставить полезную информацию для создания контента."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        research_data = response.choices[0].message.content.strip()
        # Try to parse as JSON, if fails return as is
        try:
            return json.loads(research_data)
        except json.JSONDecodeError:
            return {"raw_research": research_data}

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python researcher.py <topic>")
        sys.exit(1)

    topic = sys.argv[1]
    result = research_topic(topic)

    # Save to file
    with open("content/research.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(json.dumps(result, ensure_ascii=False, indent=2))