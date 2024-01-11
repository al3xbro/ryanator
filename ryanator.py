import discord
from discord.ext import tasks
from discord.ext import commands
from datetime import timedelta, datetime
import settings

class Client(commands.Bot):

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True 
        super().__init__(intents=intents, command_prefix='!')
        self.chat_history = []
    
    @tasks.loop(minutes=1)
    async def remove_old_messages(self):
        now = datetime.now()
        for k, message in enumerate(self.chat_history):
            if now - message[1] > timedelta(minutes=15):
                del self.chat_history[k]
    
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author != self.user:
            self.chat_history.append((message.author.name + ": " + message.content, message.created_at))

client = Client()

@client.hybrid_command(name='summarize', with_app_command=True, description='summarizes last 15 mins of chat history', aliases=['s']) 
async def summarize(self, ctx):
    summary = "endpoint"
    if not self.chat_history:
        await ctx.send("aint shit happen")
    else:
        await ctx.send(self.chat_history)

client.run(settings.token)