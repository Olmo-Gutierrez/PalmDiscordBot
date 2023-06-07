import os
import discord
import google.generativeai as palm
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
PALM_API_KEY = os.getenv("PALM_API_KEY")

intents = discord.Intents.all()
client = discord.Client(intents=intents)

palm.configure(api_key = PALM_API_KEY )

messages = []

defaults = {
    'model': 'models/chat-bison-001',
    'temperature': 0.25,
    'candidate_count': 1,
    'top_k': 40,
    'top_p': 0.95,
}

# Default discord messages:
botHelp = "# Help commands:\n\n**!help:** display a list of commands\n**\"!\"** at the start of the message makes the bot ignore the message \n\n*More commands coming soon!*"

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    

@client.event
async def on_message(message):
    print(message.content)
    if message.author.bot:
        return
    if message.content.startswith("!"):
        if message.content.startswith("!help"):
            await message.reply(botHelp)
            return
        else:
            return
    
    prompt = message.content
    messages.append(prompt)
    response = palm.chat(**defaults, context="", examples=[], messages=messages)
    
    await message.reply(response.last)
    print(response.last)

            
client.run(DISCORD_TOKEN)