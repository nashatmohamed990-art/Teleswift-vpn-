# app.py - Vercel Entry Point (Minimal)
import asyncio
from multilingual_bot import main as bot_main

# This is what Vercel expects for Python functions
async def handler(request=None):
    """Vercel serverless handler"""
    try:
        print("Starting Telegram bot...")
        await bot_main()   # This won't work perfectly on Vercel
    except Exception as e:
        print(f"Error: {e}")

# For Vercel Python runtime
app = handler
