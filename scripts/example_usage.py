#!/usr/bin/env python3
"""
Example usage of Content Factory
"""

import subprocess
import sys

def example():
    # Example topic
    topic = "Английские фразовые глаголы для начинающих"

    print("=== Content Factory Example ===")
    print(f"Generating content for: {topic}")
    print()

    # Run the content factory
    result = subprocess.run([
        sys.executable, "scripts/content_factory.py", topic
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return

    print(result.stdout)

if __name__ == "__main__":
    example()