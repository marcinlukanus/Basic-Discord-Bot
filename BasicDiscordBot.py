import random
import requests
import asyncio

from discord import Game
from discord.ext.commands import Bot

BOT_PREFIX = ("?", "!")
TOKEN = 'xxxxxxxxxxxxxxxxxx' # Removed personal token to ensure no one has access to my bot
BAD_WORDS = ['test1', 'test2', 'test3']

client = Bot(command_prefix=BOT_PREFIX)

# Allows users to ask yes/no questions and receive a random response
@client.command(name = '8ball',
                description = "Answers a yes/no question.",
                brief = "Answers from the beyond.",
                aliases = ['eight_ball', 'eightball', '8-ball'],
                pass_context = True)
async def eight_ball(context):
    possible_responses = [
        'That is a resounding no',
        'It is not looking likely',
        'Too hard to tell',
        'It is quite possible',
        'Definitely',
    ]
    await client.say(random.choice(possible_responses) + ", " + context.message.author.mention)

# Simple mathematical command that takes any given integer and returns the integer squared
@client.command(name = 'square',
                description = 'Squares any given integer.',
                brief = 'Squares any given integer.',)
async def square(number):
    squared_value = int(number) * int(number)
    await client.say(str(number) + " squared is " + str(squared_value))

# Simple API grabber command using the CoinDesk API to show current Bitcoin price in USD
@client.command(name = 'bitcoin',
                description = 'Grabs the current USD price of Bitcoin from CoinDesk.com',
                brief = 'Returns USD Bitcoin price')
async def bitcoin():
    url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
    response = requests.get(url)
    value = response.json()['bpi']['USD']['rate']
    await client.say("Bitcoin price is: $" + value)

# async def list_servers():
#     await client.wait_until_ready()
#     while not client.is_closed:
#         print("Current servers: ")
#         for server in client.servers:
#             print(server.name)
#         await asyncio.sleep(6)

# Event handling for messages
@client.event
async def on_message(message):
    # Bot will not reply to itself
    if message.author == client.user:
        return

    # If your message begins by mentioning the bot, it will reply and mention the author
    # Else if mentioned at any point in a message, just replies without mentioning the author
    if message.content.startswith(client.user.mention):
        await client.send_message(message.channel, "Hi there, " + message.author.mention)
    elif client.user.mention in message.content:
        await client.send_message(message.channel, "Did someone say my name?")

    # Have to make sure my bot is always rooting for me
    if 'MARCIN' in message.content.upper():
        await client.send_message(message.channel, "Go Marcin!")

    # I want this bot to be a moderator, so it reads every message and looks for
    # any word that may be in the BAN_WORDS array, and if there's a match, deletes
    # the message and verbally warns the user.
    for word in BAD_WORDS:
        if word.upper() in message.content.upper():
            await client.delete_message(message)
            await client.send_message(message.channel, message.author.mention + ", no swearing please.")

# Prints out information as way of displaying the bot's information
# Lets you know the bot is now online
@client.event
async def on_ready():
    # This sets the bot's game status to make it read "Playing with Fire"
    # Which is a reference to my favorite Major League Soccer team, Chicago Fire
    await client.change_presence(game = Game(name = "with Fire"))

    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

# client.loop.create_task(list_servers())

# This is what allows the bot to actually go live
client.run(TOKEN)
