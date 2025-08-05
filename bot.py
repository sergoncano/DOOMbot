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

    async def initialize_gif(self):
        self.gifmessage = await self.channel.send(
            DOOM_GIF_URL
            + f"\nCurrent player: {self.player.name}"
            + '\nuse "doom end" to exit'
        )

    async def delete_self(self):
        await self.gifmessage.delete()
        del players[self.player.id]

    async def on_message(self, message):
        print(f"Recieved {message.content}")

        if message.author == bot.user:
            return

        if message.author == self.player and message.content == "doom end":
            await self.delete_self()
            return

        if message.author != self.player:
            return

        if message.content == "w":
            self.gifmessage = await self.gifmessage.edit(
                content=self.gifmessage.content.replace("i", "wi", 1)
            )
            await message.delete()
        elif message.content == "a":
            self.gifmessage = await self.gifmessage.edit(
                content=self.gifmessage.content.replace("i", "ai", 1)
            )
            await message.delete()
        elif message.content == "s":
            self.gifmessage = await self.gifmessage.edit(
                content=self.gifmessage.content.replace("i", "si", 1)
            )
            await message.delete()
        elif message.content == "d":
            self.gifmessage = await self.gifmessage.edit(
                content=self.gifmessage.content.replace("i", "di", 1)
            )
            await message.delete()
        elif message.content == "e":
            self.gifmessage = await self.gifmessage.edit(
                content=self.gifmessage.content.replace("i", "ei", 1)
            )
            await message.delete()
        elif message.content == "q":
            self.gifmessage = await self.gifmessage.edit(
                content=self.gifmessage.content.replace("i", "qi", 1)
            )
            await message.delete()

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
        if message.content == "doom init":
            if id in players:
                return
            players[id] = BotInstance(message)
            await players[id].initialize_gif()
        else:
            if id in players:
                await players[id].on_message(message)

    bot.run(APP_TOKEN)
