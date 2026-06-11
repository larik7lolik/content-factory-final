#!/usr/bin/env python3
"""
Image Creator Agent for Content Factory
Generates cover images for content posts
"""

import json
import os
import sys
from openai import OpenAI
import requests
from dotenv import load_dotenv
load_dotenv()
from PIL import Image
from io import BytesIO

def generate_image_prompt(topic, research_data, content_data):
    """
    Generate a detailed prompt for image creation
    """
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    )

    prompt = f"""
    Create a detailed description of an image for a post on the topic: "{topic}"

    Researched information:
    {json.dumps(research_data, ensure_ascii=False, indent=2)}

    Content example:
    {json.dumps(content_data, ensure_ascii=False, indent=2)}

    Create a detailed description of the image that will be used as a cover for the post.
    Include in the description:
    - Key visual elements
    - Color palette
    - Style (minimalism, bright, professional, etc.)
    - Text elements (if needed)

    Answer in English for better compatibility with image generation models.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a designer and expert in visual content. Your task is to create descriptions for attractive post covers. Please provide the description in English for better compatibility with image generation models."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )

        image_description = response.choices[0].message.content.strip()

        # Ensure the description is in English
        if not image_description.lower().startswith(("create", "generate", "design")) and not any(char.isalpha() and ord(char) < 128 for char in image_description[:50]):
            # If it seems to be in Russian, translate it
            try:
                translate_client = OpenAI(
                    api_key=os.getenv("OPENAI_API_KEY"),
                    base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
                )

                translation_response = translate_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Translate the following text to English:"},
                        {"role": "user", "content": image_description}
                    ],
                    temperature=0.3,
                    max_tokens=300
                )

                image_description = translation_response.choices[0].message.content.strip()
            except Exception:
                # If translation fails, just proceed with original
                pass

        return image_description

    except Exception as e:
        return f"Error generating image prompt: {str(e)}"

def create_cover_image(image_description, output_path="content/cover.png"):
    """
    Create a cover image based on description
    """
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    )

    try:
        # Translate image description to English for better model understanding
        translate_client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        )

        translation_response = translate_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Translate the following Russian text to English:"},
                {"role": "user", "content": image_description}
            ],
            temperature=0.3,
            max_tokens=300
        )

        english_description = translation_response.choices[0].message.content.strip()

        response = client.images.generate(
            model="gpt-image-2",
            prompt=f"Create a professional educational cover image: {english_description}",
            size="1024x1024",  # Kept the same size for gpt-image-2
            quality="auto",  # Changed to "auto" for better compatibility
            n=1,
        )

        # Debug: print response to understand its structure
        # print(f"Response: {response}")

        if response.data and len(response.data) > 0:
            image_data = response.data[0]
            # Check if we have a URL or base64 data
            if hasattr(image_data, 'url') and image_data.url:
                image_url = image_data.url
                # Download and save image
                image_response = requests.get(image_url)
                image = Image.open(BytesIO(image_response.content))
                image.save(output_path)
                return {"status": "success", "image_path": output_path}
            elif hasattr(image_data, 'b64_json') and image_data.b64_json:
                # Handle base64 encoded image
                import base64
                image_data_bytes = base64.b64decode(image_data.b64_json)
                image = Image.open(BytesIO(image_data_bytes))
                image.save(output_path)
                return {"status": "success", "image_path": output_path}
            else:
                return {"status": "error", "message": "No valid image data in response"}
        else:
            return {"status": "error", "message": "Empty response from image generation API"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python image_creator.py <topic> <research_file> <content_file>")
        sys.exit(1)

    topic = sys.argv[1]

    # Read research data
    with open(sys.argv[2], "r", encoding="utf-8") as f:
        research_data = json.load(f)

    # Read content data
    with open(sys.argv[3], "r", encoding="utf-8") as f:
        content_data = json.load(f)

    # Generate image description
    image_description = generate_image_prompt(topic, research_data, content_data)

    # Save image description
    with open("content/image_description.txt", "w", encoding="utf-8") as f:
        f.write(image_description)

    # Create cover image
    result = create_cover_image(image_description)

    print(json.dumps(result, ensure_ascii=False, indent=2))
