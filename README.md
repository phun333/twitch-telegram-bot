# Twitch Stream Notification Bot

This bot monitors your specified Twitch streamer and sends notifications to your Telegram when they go live.

## Features

- Instant notifications when streamer goes live
- Stream title and game information
- Direct link to stream
- Checks every 2 minutes
- Spam protection (no duplicate notifications for same stream)
- Automatic reconnection
- Error recovery

## Requirements

- Python 3.x
- pip (Python package manager)
- Twitch Developer account
- Telegram bot

## Installation

1. Clone the repository:

   ```bash
   git clone [repo-url]
   cd twitch-telegram-bot
   ```

2. Create virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   # or
   .\venv\Scripts\activate  # For Windows
   ```

3. Install requirements:

   ```bash
   pip install -r requirements.txt
   ```

4. Get API credentials:

   **Twitch API Credentials:**
   - Go to [Twitch Developer Console](https://dev.twitch.tv/console)
   - Create a new application
   - Get your Client ID and Client Secret

   **Telegram Bot:**
   - Talk to [@BotFather](https://t.me/botfather)
   - Create new bot using `/newbot` command
   - Get your bot token
   - Send a message to your bot
   - Get your chat ID by visiting:
     `https://api.telegram.org/bot<BOT_TOKEN>/getUpdates`

5. Create `.env` file:

   ```properties
   TWITCH_CLIENT_ID=your_twitch_client_id
   TWITCH_CLIENT_SECRET=your_twitch_client_secret
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   TELEGRAM_CHAT_ID=your_telegram_chat_id
   TWITCH_USERNAME=favorite_streamer_username
   ```

## Usage

To start the bot:

```bash
python main.py
```

The bot will:

- Check streamer status every 2 minutes
- Send notification when stream starts
- Include stream title, game, and link in notification
- Avoid duplicate notifications for same stream
- Send initial notification if stream is live when bot starts

## Troubleshooting

If the bot encounters errors:

1. Verify credentials in `.env` file
2. Check your internet connection
3. Verify Twitch API keys are valid
4. Ensure your Telegram bot is active

## Notes

- Use tools like screen or tmux to keep the bot running in background
- Notifications are sent only once when stream starts
- Bot will wait 60 seconds and retry on errors

## Contributing

We welcome contributions to improve this project! Feel free to:

- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

Your contributions will help make this bot even better. Thank you for your interest in the project!
