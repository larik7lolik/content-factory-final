#!/usr/bin/env python3
"""
Main Content Factory Script
Orchestrates the content creation process using specialized agents
"""

import json
import os
import subprocess
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python content_factory.py <lesson_topic>")
        sys.exit(1)

    topic = sys.argv[1]
    print(f"Creating content for topic: {topic}")

    # Ensure content directory exists
    os.makedirs("content", exist_ok=True)

    # Step 1: Research the topic
    print("Step 1: Researching the topic...")
    result = subprocess.run([
        sys.executable, "agents/researcher.py", topic
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Researcher agent failed: {result.stderr}")
        sys.exit(1)

    research_data = json.loads(result.stdout)
    print("Research completed!")

    # Step 2: Create content for platforms
    print("Step 2: Creating platform-specific content...")
    result = subprocess.run([
        sys.executable, "agents/content_writer.py", topic, "content/research.json"
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Content writer agent failed: {result.stderr}")
        sys.exit(1)

    content_data = json.loads(result.stdout)
    print("Content creation completed!")

    # Step 3: Create cover image
    print("Step 3: Generating cover image...")
    result = subprocess.run([
        sys.executable, "agents/image_creator.py", topic,
        "content/research.json", "content/platform_content.json"
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Image creator agent failed: {result.stderr}")
        sys.exit(1)

    image_data = json.loads(result.stdout)
    print("Cover image generated!")

    # Step 4: Compile final output
    print("Step 4: Compiling final output...")
    result = subprocess.run([
        sys.executable, "agents/publisher.py", topic,
        "content/research.json", "content/platform_content.json", "content/cover.png"
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Publisher agent failed: {result.stderr}")
        sys.exit(1)

    final_output = json.loads(result.stdout)
    print("Final output compiled!")

    # Print summary
    print("\n=== CONTENT FACTORY RESULT ===")
    print(f"Topic: {final_output.get('topic', 'N/A')}")
    print(f"Generated at: {final_output.get('generated_at', 'N/A')}")
    print(f"Platforms covered: {', '.join(final_output.get('platforms', {}).keys())}")
    print(f"Cover image: {final_output.get('cover_image', 'N/A')}")
    print("\nFiles created:")
    print("- content/output.json")
    print("- content/cover.png")
    print("- content/research.json")
    print("- content/platform_content.json")
    print("- content/image_description.txt")

if __name__ == "__main__":
    main()