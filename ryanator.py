import discord
from discord.ext import tasks
from discord.ext import commands
from datetime import timedelta, datetime
import aiohttp

import settings

class Client(commands.Bot):

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        self.chat_history = []
        super().__init__(intents=intents, command_prefix='!')
    
    @tasks.loop(minutes=1)
    async def remove_old_messages(self):
        now = datetime.now()
        for k, message in enumerate(self.chat_history):
            if now - message[1] > timedelta(minutes=15):
                del self.chat_history[k]
    
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, ctx):
        if ctx.content != "!summarize" and ctx.content != "!cute" and ctx.content != "!gang" and ctx.content !="im thinking":
            self.chat_history.append((ctx.author.name + ": " + ctx.content, ctx.created_at))
        await self.process_commands(ctx)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.reply("not a command dumbahh")
        else:
            await ctx.reply(error)

client = Client()


@client.hybrid_command()
async def summarize(ctx: commands.Context):
    await ctx.send("im thinking")

    text_data = ""
    for message in client.chat_history:
        text_data += message[0] + "\n"

    if text_data == "":
        await ctx.reply("aint shit happen")
        return

    async with aiohttp.ClientSession(loop=ctx.bot.loop) as session:
        res = await session.post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={settings.api_key}", json={
            "contents": [
                {
                "parts": [{
                    "text": "Summarize the content of these messages as if you were a bot named ryanator:" + text_data + "\n\nryanator:"
                }]
                }
            ],
            "generationConfig": {
                "temperature": 0.9,
                "topK": 1,
                "topP": 1,
                "maxOutputTokens": 2048,
                "stopSequences": ["\n"]
            },
            "safetySettings": [
                {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
                },
                {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
                },
                {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
                },
                {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
                }
            ]
        })
        res = await res.json()
        await ctx.reply(res["candidates"][0]["content"]["parts"][0]["text"])

@client.hybrid_command()
async def cute(ctx: commands.Context):
    await ctx.send("im thinking")

    text_data = ""
    for message in client.chat_history:
        text_data += message[0] + "\n"

    if text_data == "":
        await ctx.reply("aint shit happen")
        return

    async with aiohttp.ClientSession(loop=ctx.bot.loop) as session:
        res = await session.post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={settings.api_key}", json={
            "contents": [
                {
                "parts": [{
                    "text": "Respond to these messages like you were a cute e-girl named ryanator who only speaks in lowercase:\n\n" + text_data + "\n\nryanator:"
                }]
                }
            ],
            "generationConfig": {
                "temperature": 0.9,
                "topK": 1,
                "topP": 1,
                "maxOutputTokens": 2048,
                "stopSequences": ["\n"]
            },
            "safetySettings": [
                {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
                },
                {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
                },
                {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
                },
                {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
                }
            ]
        })
        res = await res.json()
        await ctx.reply(res["candidates"][0]["content"]["parts"][0]["text"])

@client.hybrid_command()
async def gang(ctx: commands.Context):
    await ctx.send("im thinking")

    text_data = ""
    for message in client.chat_history:
        text_data += message[0] + "\n"

    if text_data == "":
        await ctx.reply("aint shit happen")
        return

    async with aiohttp.ClientSession(loop=ctx.bot.loop) as session:
        res = await session.post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={settings.api_key}", json={
            "contents": [
                {
                "parts": [{
                    "text": "Respond to these messages like you were a hard gangster named ryanator:\n\n" + text_data + "\n\nryanator:"
                }]
                }
            ],
            "generationConfig": {
                "temperature": 0.9,
                "topK": 1,
                "topP": 1,
                "maxOutputTokens": 2048,
                "stopSequences": ["\n"]
            },
            "safetySettings": [
                {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
                },
                {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
                },
                {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
                },
                {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
                }
            ]
        })
        res = await res.json()
        await ctx.reply(res["candidates"][0]["content"]["parts"][0]["text"])

client.run(settings.discord_token)