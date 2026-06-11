# Content Factory Skill for Claude Code

## Overview

This skill helps Claude Code work effectively with the Content Factory repository. It provides documentation and helper scripts for understanding project structure, running content generation, modifying agents, updating documentation, checking for errors, and preparing for publication.

## Project Overview

Content Factory is an AI-powered content generation system designed for EdTech marketers. It automates the creation of platform-specific content and cover images based on educational topics. Users provide a lesson topic, and the system generates ready-to-publish posts for Telegram, VK, Yandex Zen, Blog, and TikTok within 3-5 minutes, saving 2-3 hours of manual work.

## Project Structure

```
content-factory/
├── agents/              # Specialized AI agents
│   ├── researcher.py     # Researches lesson topics
│   ├── content_writer.py # Creates platform-specific content
│   ├── image_creator.py  # Generates cover images
│   └── publisher.py      # Compiles final output
├── scripts/             # Main execution scripts
│   └── content_factory.py # Orchestrates the content creation process
├── skills/              # Additional Claude Code skills
├── content/             # Generated content output
├── .claude/             # Claude Code configuration
│   └── skills/          # Custom skills
│       └── content-factory/
│           ├── SKILL.md          # Skill documentation (this file)
│           ├── metadata.yaml      # Skill metadata
│           ├── manifest.json     # Skill manifest
│           ├── content_factory_skill.py # Python helper script
│           └── content-factory.sh # Bash command script
├── .env                 # API keys and configuration
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## Content Generation Commands

### Using Helper Scripts
```bash
# Generate content for a specific topic
./.claude/skills/content-factory/content-factory.sh generate "Your Lesson Topic"

# Run researcher agent
./.claude/skills/content-factory/content-factory.sh research "Your Topic"

# Check project status
./.claude/skills/content-factory/content-factory.sh status
```

### Direct Commands
```bash
# Generate content for a specific topic
python scripts/content_factory.py "Your Lesson Topic"

# Example
python scripts/content_factory.py "French Grammar: Passé Composé vs Imparfait"
```

### Individual Agent Execution
```bash
# Run researcher agent
python agents/researcher.py "Topic"

# Run content writer agent
python agents/content_writer.py "Topic" content/research.json

# Run image creator agent
python agents/image_creator.py "Topic" content/research.json content/platform_content.json

# Run publisher agent
python agents/publisher.py "Topic" content/research.json content/platform_content.json content/cover.png
```

## Adding New Agents

### Steps to Add a New Agent

1. **Create the agent file** in `agents/` directory:
   ```bash
   touch agents/new_agent.py
   ```

2. **Implement the agent structure**:
   ```python
   #!/usr/bin/env python3
   import json
   import os
   import sys
   from openai import OpenAI
   
   def agent_function(param1, param2):
       """
       Describe what this agent does
       """
       # Implementation here
       pass
   
   if __name__ == "__main__":
       # Handle command line arguments
       if len(sys.argv) != expected_args_count:
           print("Usage: python new_agent.py <param1> <param2>")
           sys.exit(1)
       
       # Parse arguments
       param1 = sys.argv[1]
       # ...
       
       # Execute agent function
       result = agent_function(param1, param2)
       
       # Output result
       print(json.dumps(result, ensure_ascii=False, indent=2))
   ```

3. **Integrate with main pipeline** in `scripts/content_factory.py`:
   - Add import or subprocess call
   - Update orchestration logic
   - Handle input/output appropriately

4. **Update documentation**:
   - Modify README.md
   - Update agent list in documentation

## Updating Documentation

### README.md Updates
When making changes to the project, update README.md to reflect:
- New features or capabilities
- Modified installation or usage instructions
- Updated project structure information
- Changes to the team or contributors

### Documentation Structure
The README.md should maintain the following sections:
1. Project overview (Формула кейса)
2. Target audience (Для кого)
3. MVP and future development (MVP и будущее развитие)
4. Screenshots (Скриншоты работы)
5. Development roadmap (Roadmap развития)
6. Technical instructions (installation, usage, etc.)

## JSON Contract Rules

### Output Format Standards

1. **Platform Content Structure** (`content/platform_content.json`):
   ```json
   {
     "Telegram": "String content for Telegram",
     "VK": {
       "заголовок": "Post title",
       "текст": "Post content",
       "призыв": "Call to action"
     },
     "Дзен": {
       "заголовок": "Article title",
       "подзаголовки": ["Subtitle 1", "Subtitle 2"],
       "текст": "Full article content"
     },
     "Блог": {
       "заголовок": "Blog post title",
       "текст": "Full blog content"
     },
     "TikTok": {
       "сценарий": "TikTok script with hashtags"
     }
   }
   ```

2. **Final Output Structure** (`content/output.json`):
   ```json
   {
     "topic": "Lesson topic",
     "generated_at": "ISO timestamp",
     "cover_image": "content/cover.png",
     "platforms": {
       "telegram": "Content for Telegram",
       "vk": {"заголовок": "...", "текст": "...", "призыв": "..."},
       "yandex_zen": {"заголовок": "...", "подзаголовки": [...], "..."},
       "blog": {"заголовок": "...", "текст": "..."},
       "tiktok": {"сценарий": "..."}
     }
   }
   ```

3. **Naming Conventions**:
   - Platform keys in platform_content.json: Native language (Telegram, VK, etc.)
   - Platform keys in output.json: Consistent lowercase English (telegram, vk, yandex_zen, blog, tiktok)

### Validation Guidelines

- All JSON output must be valid and parseable
- Platform keys must match expected names
- Timestamps must be in ISO format
- File paths must be relative to project root
- UTF-8 encoding for all text content

## Error Checking

### Common Issues and Solutions

1. **API Key Errors**:
   - Check that `.env` file exists and contains valid API keys
   - Verify that `OPENAI_API_KEY` and `OPENAI_BASE_URL` are set correctly
   - Test connectivity with `curl` command to the API endpoint

2. **JSON Parsing Errors**:
   - Check that generated JSON files are valid with `python -m json.tool`
   - Ensure the content writer agent is producing valid JSON without markdown wrappers
   - Validate platform keys match expected naming conventions

3. **Image Generation Failures**:
   - Ensure the correct model is specified (`gpt-image-2` for ProxyAPI)
   - Check that prompts are in English for better model understanding
   - Verify `size` and `quality` parameters are supported by the API

4. **File Permission Errors**:
   - Ensure the `content/` directory is writable
   - Check that all Python scripts have execute permissions
   - Verify that dependent libraries are installed

### Diagnostics Commands
```bash
# Check project status
./.claude/skills/content-factory/content-factory.sh status

# Validate JSON output
python -m json.tool content/output.json

# Check environment variables
cat .env

# Test API connectivity
curl -H "Authorization: Bearer $OPENAI_API_KEY" $OPENAI_BASE_URL/models
```

## GitHub Publishing Steps

### Pre-Publication Checklist

1. **Clean repository**:
   ```bash
   # Remove any sensitive files
   git clean -fd
   
   # Check for uncommitted changes
   git status
   ```

2. **Update version information**:
   - Increment version in README.md if applicable
   - Update CHANGELOG.md if it exists
   - Check that all links are valid

3. **Verify functionality**:
   ```bash
   # Test content generation
   python scripts/content_factory.py "Test Topic"
   
   # Verify output files
   ls -la content/
   ```

4. **Documentation review**:
   - Proofread README.md
   - Ensure all commands work as documented
   - Verify project structure is accurately described

### Publishing Process

1. **Commit and push changes**:
   ```bash
   git add .
   git commit -m "Prepare for release vX.X.X"
   git push origin main
   ```

2. **Create a GitHub release**:
   - Go to GitHub repository Releases page
   - Click "Draft a new release"
   - Create a new tag (e.g., v1.0.0)
   - Write release notes summarizing changes
   - Publish release

3. **Update package metadata** (if applicable):
   - Update setup.py version
   - Update PyPI package if distributed there

### Post-Publication

1. **Monitor issues** for user feedback
2. **Update documentation** based on user questions
3. **Plan next iteration** based on feedback