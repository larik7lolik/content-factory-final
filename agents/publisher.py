#!/usr/bin/env python3
"""
Publisher Agent for Content Factory
Formats and organizes final content output
"""

import json
import os
import sys

def compile_final_output(topic, research_data, content_data, image_path="content/cover.png"):
    """
    Compile all content into final output format
    """
    final_output = {
        "topic": topic,
        "generated_at": __import__('datetime').datetime.now().isoformat(),
        "cover_image": image_path,
        "platforms": {}
    }

    # Process content for each platform
    try:
        # Assuming content_data has platform-specific content
        if "telegram" in content_data:
            final_output["platforms"]["telegram"] = content_data["telegram"]
        elif "Telegram" in content_data:
            final_output["platforms"]["telegram"] = content_data["Telegram"]

        if "vk" in content_data:
            final_output["platforms"]["vk"] = content_data["vk"]
        elif "VK" in content_data:
            final_output["platforms"]["vk"] = content_data["VK"]

        if "дзен" in content_data:
            final_output["platforms"]["yandex_zen"] = content_data["дзен"]
        elif "Дзен" in content_data:
            final_output["platforms"]["yandex_zen"] = content_data["Дзен"]

        if "блог" in content_data:
            final_output["platforms"]["blog"] = content_data["блог"]
        elif "Блог" in content_data:
            final_output["platforms"]["blog"] = content_data["Блог"]

        if "tiktok" in content_data:
            final_output["platforms"]["tiktok"] = content_data["tiktok"]
        elif "TikTok" in content_data:
            final_output["platforms"]["tiktok"] = content_data["TikTok"]

        # If we don't find platform-specific keys, we'll put the whole content
        if not final_output["platforms"]:
            final_output["platforms"]["general"] = content_data

    except Exception as e:
        final_output["error"] = f"Error processing content data: {str(e)}"
        final_output["raw_content"] = content_data

    return final_output

if __name__ == "__main__":
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print("Usage: python publisher.py <topic> <research_file> <content_file> [image_file]")
        sys.exit(1)

    topic = sys.argv[1]

    # Read research data
    with open(sys.argv[2], "r", encoding="utf-8") as f:
        research_data = json.load(f)

    # Read content data
    with open(sys.argv[3], "r", encoding="utf-8") as f:
        content_data = json.load(f)

    # Get image path if provided
    image_path = sys.argv[4] if len(sys.argv) == 5 else "content/cover.png"

    # Compile final output
    result = compile_final_output(topic, research_data, content_data, image_path)

    # Save to output file
    with open("content/output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(json.dumps(result, ensure_ascii=False, indent=2))