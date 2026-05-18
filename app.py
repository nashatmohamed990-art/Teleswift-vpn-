# app.py - Vercel compatible (minimal)
import asyncio
from multilinguall_bot import main

async def handler(request):
    # This is mostly a placeholder - the bot won't stay alive long
    return {
        "statusCode": 200,
        "body": "Bot started (but may not stay alive on Vercel)"
    }

# Vercel needs this
app = handler

# Try to start the bot anyway
if __name__ == "__main__":
    asyncio.run(main())
    
