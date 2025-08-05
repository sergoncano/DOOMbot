import os

import discord
import dotenv

dotenv.load_dotenv()
APP_TOKEN = str(os.getenv("APP_TOKEN"))

DOOM_GIF_URL = "https://doom.p2r3.com/i.webp"

intents = discord.Intents._from_value(32768)

bot = discord.Bot(intents=discord.Intents.all())

currentplayer = None
gifmessage = None
lookForMessages = False


@bot.event
async def on_ready():
    print(f"{bot.user} is running")


@bot.event
async def on_message(message):
    print(f"Recieved {message.content}")
    global currentplayer
    global lookForMessages

    if lookForMessages:
        print("Found my own message")
        global gifmessage
        gifmessage = message
        lookForMessages = False
        return

    if message.author == bot.user:
        return

    if message.content == "doom init" and currentplayer is None:
        currentplayer = message.author
        lookForMessages = True
        await message.channel.send(
            DOOM_GIF_URL
            + f"\nCurrent player: {message.author.name}"
            + '\nuse "doom end" to exit'
        )

    if (
        message.author == currentplayer
        and message.content == "doom end"
        and currentplayer is not None
    ):
        currentplayer = None
        gifmessage = None
        return

    if currentplayer is None or message.author != currentplayer:
        return

    if message.content == "w":
        await gifmessage.edit(content=gifmessage.content.replace("i", "wi", 1))
    elif message.content == "a":
        await gifmessage.edit(content=gifmessage.content.replace("i", "ai", 1))
    elif message.content == "s":
        await gifmessage.edit(content=gifmessage.content.replace("i", "si", 1))
    elif message.content == "d":
        await gifmessage.edit(content=gifmessage.content.replace("i", "di", 1))
    elif message.content == "e":
        await gifmessage.edit(content=gifmessage.content.replace("i", "ei", 1))
    elif message.content == "q":
        await gifmessage.edit(content=gifmessage.content.replace("i", "qi", 1))


bot.run(APP_TOKEN)
