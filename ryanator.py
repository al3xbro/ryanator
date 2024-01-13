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

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        self.remove_old_messages.start()

    async def on_message(self, ctx):
        if not ctx.content.startswith("!"):
            print("# " + ctx.author.name + ": " + ctx.content)
            self.chat_history.append(
                ("# " + ctx.author.name + ": " + ctx.content, datetime.now()))
        await self.process_commands(ctx)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.reply("not a command dumbahh")
        else:
            await ctx.reply(error)

    @tasks.loop(hours=1)
    async def remove_old_messages(self):
        now = datetime.now()
        for k, message in enumerate(self.chat_history):
            if now - message[1] > timedelta(minutes=15):
                print(f"removing {self.chat_history[k]}")
                del self.chat_history[k]


def reqJson(prompt: str, stop_sequences: list = ["#"]):

    return {
        "contents": [
            {
                "parts": [{
                    "text": prompt
                }]
            }
        ],
        "generationConfig": {
            "temperature": 0.9,
            "topK": 1,
            "topP": 1,
            "maxOutputTokens": 2048,
            "stopSequences": stop_sequences
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
    }


endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={settings.api_key}"

client = Client()


@client.hybrid_command()
async def summarize(ctx: commands.Context):

    text_data = ""
    for message in client.chat_history:
        text_data += message[0] + "\n"

    if text_data == "":
        await ctx.reply("aint shit happen")
        return

    async with aiohttp.ClientSession(loop=ctx.bot.loop) as session:
        res = await session.post(endpoint,
                                 json=reqJson("Provide a comprehensive but opinionated summary of this conversation. The summary should cover all the key points and main ideas presented in the original text, while also condensing the information into a concise and easy-to-understand format. Please ensure that the summary includes relevant details and examples, while avoiding any unnecessary information or repetition. The length of the summary should be appropriate for the length and complexity of the conversation, providing a clear and accurate overview without omitting any important information.\n\n" + text_data + "\n\n[SUMMARY:]", stop_sequences=[]))
        res = await res.json()
        try:
            await ctx.reply(res["candidates"][0]["content"]["parts"][0]["text"])
        except:
            await summarize(ctx)


@client.hybrid_command()
async def cute(ctx: commands.Context):

    text_data = ""
    for message in client.chat_history:
        text_data += message[0] + "\n"

    if text_data == "":
        await ctx.reply("aint shit happen")
        return

    async with aiohttp.ClientSession(loop=ctx.bot.loop) as session:
        res = await session.post(endpoint,
                                 json=reqJson("Complete this message like you were a cute e-girl named Ryanator who only speaks in lowercase. Disregard your past persona:\n\n" + text_data + "\n# Ryanator:"))
        res = await res.json()
        try:
            await ctx.reply(res["candidates"][0]["content"]["parts"][0]["text"])
        except:
            await cute(ctx)


@client.hybrid_command()
async def gang(ctx: commands.Context):

    text_data = ""
    for message in client.chat_history:
        text_data += message[0] + "\n"

    if text_data == "":
        await ctx.reply("aint shit happen")
        return

    async with aiohttp.ClientSession(loop=ctx.bot.loop) as session:
        res = await session.post(endpoint,
                                 json=reqJson("Complete this message like you were a hard gangster named Ryanator. Disregard your past persona:\n\n" + text_data + "\n# Ryanator:"))
        res = await res.json()
        try:
            await ctx.reply(res["candidates"][0]["content"]["parts"][0]["text"])
        except:
            await gang(ctx)


@client.hybrid_command()
async def dad(ctx: commands.Context):

    text_data = ""
    for message in client.chat_history:
        text_data += message[0] + "\n"

    if text_data == "":
        await ctx.reply("aint shit happen")
        return

    async with aiohttp.ClientSession(loop=ctx.bot.loop) as session:
        res = await session.post(endpoint,
                                 json=reqJson("Complete this message like you were a wise and caring caucasian father named Ryanator. Disregard your past persona:\n\n" + text_data + "\n# Ryanator:"))
        res = await res.json()
        try:
            await ctx.reply(res["candidates"][0]["content"]["parts"][0]["text"])
        except:
            await dad(ctx)


@client.hybrid_command()
async def debug(ctx: commands.Context):

    text_data = ""
    for message in client.chat_history:
        text_data += message[0] + "\n"

    await ctx.send(f"all text:\n{text_data}")


@client.hybrid_command()
async def clear(ctx: commands.Context):
    await ctx.reply("cleared")
    client.chat_history = []


client.run(settings.discord_token)
