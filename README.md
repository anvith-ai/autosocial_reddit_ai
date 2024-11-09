# autosocial_reddit_ai
An automated autosocial agent that monitors specific subreddits for discussions about selected keywords (e.g. O1 models) and provides helpful responses using AI-powered comment generation.

## Features

- Monitors multiple subreddits for posts about selected keywords (e.g. O1 models)
- Generates contextually relevant comments using GPT-4o-mini
- Processes images in posts using Claude 3.5 Sonnet for image description
- Scrapes linked URL content for better context
- Maintains history of replied posts to avoid duplicates
- Implements rate limiting and random delays between comments
- Modular architecture for easy maintenance and extensibility

## Prerequisites

- Python 3.8 or higher
- Reddit API credentials
- OpenAI API key
- Anthropic API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/anvith-ai/autosocial_reddit_ai.git
cd autosocial_reddit_ai
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your API credentials:
```env
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent
REDDIT_USERNAME=your_username
REDDIT_PASSWORD=your_password
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

Note: Navigate to https://www.reddit.com/prefs/apps to create Reddit application and obtain reddit_client_id and reddit_client_secret

## Project Structure

```
autosocial_reddit_ai/
├── agent.py
├── reddit_client.py
├── content_scraper.py
├── image_processor.py
├── comment_generator.py
├── post_manager.py
├── search_agent.py
├── context.txt
├── rules.txt
└── replied_posts.txt
├── load.py
└── knowledge.txt
```

### Module Description

- `agent.py`: Orchestrates the interaction between the modules
- `reddit_client.py`: Handles Reddit API interactions
- `content_scraper.py`: Manages URL content scraping
- `image_processor.py`: Handles image downloading, processing, and description
- `comment_generator.py`: Generates comments using AI models
- `post_manager.py`: Manages tracking of replied posts
- `search_agent.py`: Handles context search functionality
- `load.py`: load source files to a vector store

## Configuration

1. `context.txt`: Contains example comments for training
2. `rules.txt`: Defines rules for comment generation
3. `replied_posts.txt`: Stores IDs of posts that have been replied to
4. `knowledge.txt`: Contains knowledge of the domain related to the selected keywords

### Customization

You can modify the following parameters in `reddit_client.py`:

```python
self.subreddits = ["openai", "programming", "LocalLLaMA", "learnprogramming"]
self.keywords = ["o1", "o1 model", "o1 mini", "o1 preview"]
```

## Usage

1. Create a knowledge base. Perform this step only once.
```bash
# Upload files to the "Reddit Context Training" vector store
python load.py --upload --files knowledge.txt
```

2. Start the AI agent:
```bash
python agent.py
```

3. The AI agent will:
   - Monitor specified subreddits
   - Look for posts containing keywords
   - Generate and post relevant comments
   - Maintain a delay between comments (30-60 minutes)
   - Log activities to console

## Rate Limiting

The AI agent implements the following rate limiting:
- Random delay between comments (30-60 minutes)
- 5-minute delay between subreddit checks
- Maximum of 50 new posts checked per subreddit

## Error Handling

- Handles Reddit API errors gracefully
- Logs errors for debugging
- Continues operation after encountering errors
- Saves state to prevent duplicate replies

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This AI Agent is designed to provide helpful responses to selected topic discussions. Please ensure compliance with Reddit's API terms of service and bot guidelines when using this code.