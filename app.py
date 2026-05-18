from multilinguall_bot import main
import asyncio
import os

# Vercel needs a top-level 'app'
async def handler(request):
    return {"statusCode": 200, "body": "Bot is running"}

app = handler

# Try to start the bot (won't last long)
if __name__ == "__main__":
    asyncio.run(main())
