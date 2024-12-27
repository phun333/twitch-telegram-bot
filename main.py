import os
import requests
from dotenv import load_dotenv
from telegram.ext import Application
import asyncio
import logging
from datetime import datetime, timezone

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Environment variables
TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
TWITCH_CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TWITCH_USERNAME = os.getenv('TWITCH_USERNAME')

class TwitchAPI:
    def __init__(self):
        self.access_token = None
        self.headers = None
        self.last_stream_status = False
        self.first_check = True

    async def get_access_token(self):
        url = 'https://id.twitch.tv/oauth2/token'
        params = {
            'client_id': TWITCH_CLIENT_ID,
            'client_secret': TWITCH_CLIENT_SECRET,
            'grant_type': 'client_credentials'
        }
        
        response = requests.post(url, params=params)
        data = response.json()
        self.access_token = data['access_token']
        self.headers = {
            'Client-ID': TWITCH_CLIENT_ID,
            'Authorization': f'Bearer {self.access_token}'
        }

    async def check_stream_status(self):
        if not self.headers:
            await self.get_access_token()

        url = f'https://api.twitch.tv/helix/streams?user_login={TWITCH_USERNAME}'
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 401:
            await self.get_access_token()
            response = requests.get(url, headers=self.headers)
        
        data = response.json()
        is_live = len(data['data']) > 0
        
        stream_data = None
        should_notify = False

        if is_live:
            stream_data = data['data'][0]
            if not self.last_stream_status or self.first_check:
                should_notify = True
        
        self.last_stream_status = is_live
        self.first_check = False
        return should_notify, stream_data

async def send_telegram_message(text):
    bot = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    async with bot:
        await bot.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)

async def check_stream_loop():
    twitch_api = TwitchAPI()
    logger.info("Bot started monitoring Twitch channel: %s", TWITCH_USERNAME)
    
    while True:
        try:
            should_notify, stream_data = await twitch_api.check_stream_status()
            
            if should_notify and stream_data:
                message = (
                    f"🔴 {TWITCH_USERNAME} is now live on Twitch!\n"
                    f"Title: {stream_data['title']}\n"
                    f"Playing: {stream_data['game_name']}\n"
                    f"Watch here: https://twitch.tv/{TWITCH_USERNAME}"
                )
                await send_telegram_message(message)
                logger.info("Sent notification for stream going live")
            
            # Check every 2 minutes
            await asyncio.sleep(120)
            
        except Exception as e:
            logger.error(f"Error occurred: {str(e)}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(check_stream_loop()) 