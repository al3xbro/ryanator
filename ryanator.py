import asyncio
import discord
from discord.ext import tasks
from discord.ext import commands
from datetime import timedelta, datetime
import together
import aiohttp

import settings

together.api_key = settings.togetherai_key

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
        if ctx.author != self.user and ctx.content != "!summarize" and ctx.content != "!cute":
            self.chat_history.append((ctx.author.name + ": " + ctx.content, ctx.created_at))
        await self.process_commands(ctx)

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
        res = await session.post("https://api.together.xyz/inference", json={
            "model": "togethercomputer/llama-2-70b-chat",
            "max_tokens": 512,
            "prompt": "Give a short summary of the content of these text messages:\n[" + text_data + "]\n[SUMMARY]:",
            "request_type": "language-model-inference",
            "temperature": 0.15,
            "top_p": 0.7,
            "top_k": 50,
            "repetition_penalty": 1,
            "stop": [
                "[/INST]",
                "</s>"
            ],
            "negative_prompt": "",
            "sessionKey": "2e59071178ae2b05e68015136fb8045df30c3680",
            "safety_model": "",
            "repetitive_penalty": 1,
            "update_at": "2023-10-28T20:07:51.077Z"
            }, headers={
                "Authorization": "Bearer " + settings.togetherai_key,
        })
        res = await res.json()
        await ctx.reply(res["output"]["choices"][0]["text"])

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
        res = await session.post("https://api.together.xyz/inference", json={
            "model": "togethercomputer/llama-2-70b-chat",
            "max_tokens": 512,
            "prompt": "Reply to these messages as if you were a cute e-girl named ryanator who only speaks in lowercase:\n[" + text_data + "]\n[REPLY]:",
            "request_type": "language-model-inference",
            "temperature": 0.15,
            "top_p": 0.7,
            "top_k": 50,
            "repetition_penalty": 1,
            "stop": [
                "[/INST]",
                "</s>"
            ],
            "negative_prompt": "",
            "sessionKey": "2e59071178ae2b05e68015136fb8045df30c3680",
            "safety_model": "",
            "repetitive_penalty": 1,
            "update_at": "2023-10-28T20:07:51.077Z"
            }, headers={
                "Authorization": "Bearer " + settings.togetherai_key,
        })
        res = await res.json()
        await ctx.reply(res["output"]["choices"][0]["text"])

client.run(settings.token)