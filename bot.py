import os
import discord
import dotenv

class BotInstance:
    gifmessage = None
    player = None
    channel = None

    def __init__(self, message):
        self.player = message.author
        self.channel = message.channel

    async def initialize(self):
        self.gifmessage = await self.channel.send(
            DOOM_GIF_URL
        )

    async def doom_exit(self):
        await self.gifmessage.delete()
        del players[self.player.id]

    @staticmethod
    async def doom_help(channel):
        help_message = '''
**Commands**
**Doom init**: start a DOOM game
**Doom back**: go back to the previous state of the game
**Doom exit**: exit your ongoing doom game
**Game controls**:
    -W: Move forth
    -S: Move back
    -A: Move left
    -D: Move right
    -Q: Fire weapon
    -E: Open door
All commands are case insensitive'''
        await channel.send(help_message)

    async def doom_back(self):
        if self.gifmessage.content[-7] == "/":
            return
        self.gifmessage = await self.gifmessage.edit(self.gifmessage.content[:-7] + self.gifmessage.content[-6:])

    async def doom_control(self, message):
        controls = ["w","a","s","d","e","q"]
        for key in controls:
            if message.content == key:
                self.gifmessage = await self.gifmessage.edit(
                    content=self.gifmessage.content.replace("i", key + "i", 1)
                )
                await message.delete()

    async def doom_command(self, message):
        text = message.content.lower()
        if text == "doom exit":
            await self.doom_exit()
            await message.delete()
        elif text == "doom back":
            await self.doom_back()
            await message.delete()

    async def on_message(self, message):
        print(f"Recieved {message.content}")

        if message.author == bot.user:
            return

        if message.author == self.player and message.content.lower().startswith("doom"):
            await self.doom_command(message)
            return

        if message.author == self.player:
            await self.doom_control(message)

        

if __name__ == "__main__":
    dotenv.load_dotenv()
    APP_TOKEN = str(os.getenv("APP_TOKEN"))

    DOOM_GIF_URL = "https://doom.p2r3.com/i.webp"

    intents = discord.Intents._from_value(32768)

    bot = discord.Bot(intents=discord.Intents.all())

    players = {}

    @bot.event
    async def on_ready():
        print(f"{bot.user} is running")

    @bot.event
    async def on_message(message):
        id = message.author.id
        text = message.content.lower()
        if text == "doom init":
            if id in players:
                return
            players[id] = BotInstance(message)
            await players[id].initialize()
        elif text == "doom help":
            await BotInstance.doom_help(message.channel)
        else:
            if id in players:
                await players[id].on_message(message)

    bot.run(APP_TOKEN)
