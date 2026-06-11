# Content Factory Skill

This skill automates the creation of marketing content for EdTech professionals across multiple platforms.

## Usage

Invoke with: `/content-factory`

## Description

The Content Factory skill transforms a lesson topic into ready-to-publish content for 5 platforms:
- Telegram
- VK
- Дзen
- Blog
- TikTok

The output includes:
- `content/output.json` - Content for all platforms
- `content/cover.png` - Generated cover image

## How it works

1. User provides a lesson topic
2. System coordinates 4 specialized agents:
   - Researcher: Gathers relevant information about the topic
   - Content Writer: Creates platform-specific content
   - Image Creator: Generates a cover image
   - Publisher: Formats and organizes the final output
3. Final content is saved to the content/ directory