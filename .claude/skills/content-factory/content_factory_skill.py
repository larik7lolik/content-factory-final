#!/usr/bin/env python3
"""
Content Factory Skill for Claude Code
Command-line interface for common Content Factory operations
"""

import argparse
import subprocess
import sys
import os
import json

def run_content_generation(topic):
    """Run the main content generation pipeline"""
    try:
        result = subprocess.run([
            sys.executable, "scripts/content_factory.py", topic
        ], capture_output=True, text=True, cwd=os.getcwd())

        if result.returncode == 0:
            print("✅ Content generation completed successfully!")
            print(result.stdout)
            return True
        else:
            print("❌ Content generation failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running content generation: {e}")
        return False

def run_researcher(topic):
    """Run only the researcher agent"""
    try:
        result = subprocess.run([
            sys.executable, "agents/researcher.py", topic
        ], capture_output=True, text=True, cwd=os.getcwd())

        if result.returncode == 0:
            print("✅ Research completed successfully!")
            research_data = json.loads(result.stdout)
            print(json.dumps(research_data, ensure_ascii=False, indent=2))
            return True
        else:
            print("❌ Research failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running researcher: {e}")
        return False

def check_project_status():
    """Check project files and structure"""
    print("🔍 Checking project status...")

    required_files = [
        "agents/researcher.py",
        "agents/content_writer.py",
        "agents/image_creator.py",
        "agents/publisher.py",
        "scripts/content_factory.py",
        ".env"
    ]

    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)

    if missing_files:
        print("❌ Missing files:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    else:
        print("✅ All required files present")
        return True

def main():
    parser = argparse.ArgumentParser(description="Content Factory Skill for Claude Code")
    parser.add_argument("action", choices=["generate", "research", "status"],
                       help="Action to perform")
    parser.add_argument("--topic", "-t", help="Lesson topic for content generation/research")

    args = parser.parse_args()

    if args.action == "status":
        check_project_status()
    elif args.action == "generate":
        if not args.topic:
            print("❌ Topic is required for content generation")
            return 1
        if run_content_generation(args.topic):
            return 0
        else:
            return 1
    elif args.action == "research":
        if not args.topic:
            print("❌ Topic is required for research")
            return 1
        if run_researcher(args.topic):
            return 0
        else:
            return 1

if __name__ == "__main__":
    sys.exit(main())