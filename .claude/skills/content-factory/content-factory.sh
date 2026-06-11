#!/bin/bash

# Content Factory Skill Command
# Usage: content-factory [action] [options]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")/../../.."
PYTHON_SCRIPT="$SCRIPT_DIR/content_factory_skill.py"

case "$1" in
    generate)
        if [ -z "$2" ]; then
            echo "Usage: content-factory generate \"<topic>\""
            exit 1
        fi
        python3 "$PYTHON_SCRIPT" generate --topic "$2"
        ;;
    research)
        if [ -z "$2" ]; then
            echo "Usage: content-factory research \"<topic>\""
            exit 1
        fi
        python3 "$PYTHON_SCRIPT" research --topic "$2"
        ;;
    status)
        python3 "$PYTHON_SCRIPT" status
        ;;
    help|*)
        echo "Content Factory Skill for Claude Code"
        echo ""
        echo "Usage:"
        echo "  content-factory generate \"<topic>\"    Generate content for all platforms"
        echo "  content-factory research \"<topic>\"    Research a topic"
        echo "  content-factory status               Check project status"
        echo ""
        echo "Examples:"
        echo "  content-factory generate \"French Grammar: Passé Composé vs Imparfait\""
        echo "  content-factory research \"Introduction to Spanish Verbs\""
        ;;
esac