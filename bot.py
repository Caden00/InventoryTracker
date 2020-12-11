# This file serves as the code that helps the bot gain connection to Discord

import asyncio
import json
import os
import Request_Headers
import Stock
import threading

from dotenv import load_dotenv
from discord.ext import commands

# We use a dotenv file to store the bot's token rather than having it hardcoded in this file
# Obviously, the env file would not be public
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


# Create a command handler object, initialized with a prefix
bot = commands.Bot(command_prefix='!')


# Function used for loading the dictionary of channels provided in a json
def load_channels():
    # Attempt to open file, located in the cwd
    if os.path.exists('channels.json'):
        file = open('channels.json')
        channels = json.load(file)
    else:
        print('Failed to load file \'channels.json\', creating the file instead.')
        channels = []
        file = open('channels.json', 'w+')
        json.dump(channels, file)

    file.close()
    return channels


# Function used for saving the list of channels provided in a json
def save_channels():
    with open('channels.json', 'w') as f:
        json.dump(notify_channels, f)
        f.close()


# Once the bot connects, print a message to console stating as such
@bot.event
async def on_ready():
    global bot_running
    bot_running = True
    print('{} has connected to Discord!'.format(bot.user))


# Use an event loop to constantly check if the products are available
# Once they do become available, send a message in designated channels
# Designated channels are declared using a command created below
async def check_for_stock():
    stock_check = Stock.Check_Stock(Stock.product_page, Request_Headers.headers)
    stock_cache = False
    current_stock = stock_check.stock()

    # Have the thread sleep initially, to hopefully let the bot connect before checking, in case of immediate availability
    await asyncio.sleep(10)

    # Ensure this keeps looping while the bot is running
    while bot_running:
        # On a 10 second interval, check for availability
        while current_stock == stock_cache:
            await asyncio.sleep(10)
            current_stock = stock_check.stock()

        # Once the stock changes and breaks the loop, update the stock_cache and send updates to designated channels
        stock_cache = current_stock
        if current_stock is True:
            print('In stock')
            message = 'Products are now available!'
        else:
            print('Out of stock')
            message = 'Products are no longer available!'

        for channel_id in notify_channels:
            channel = bot.get_channel(channel_id)
            asyncio.run_coroutine_threadsafe(channel.send(message), bot.loop)


# Simple command example: ping
# Command name used to determine what the user must type to activate the command. In this case: !ping
# Command help used to provide more information if the user asks for help with this command.
# The argument, ctx, stands for context and contains contextual information from where the command was sent from
# Context contains things such as the user who called the command, which server and channel it is in, etc.
# Using ctx.send directly sends a message in the same channel and server that the command was used in
# Lastly, everything should be awaited and using async to ensure the bot can pay attention to multiple events
@bot.command(name='ping', help='Responds with pong - simple command to test bot connection and/or latency.')
async def ping(ctx):
    await ctx.send('pong')


# Command to check stock on demand
# Will send a message depending on whether or not the product is in stock.
@bot.command(name='stock', help='Responds with whether the products are in stock or not')
async def stock(ctx):
    stock_check = Stock.Check_Stock(Stock.product_page, Request_Headers.headers)
    if stock_check.stock():
        await ctx.send('Products are in stock.')
    else:
        await ctx.send('Products are NOT in stock.')


# Command used to store "designated channels" for alerting when products are in stock
@bot.command(name='notify', help='Tells the bot to notify product availability in the channel the command was used in')
async def notify(ctx):
    # Check if the guild ID exists in the dictionary first, then check if the channel id exists as well
    if ctx.channel.id in notify_channels:
        # If so, then this command should do nothing
        await ctx.send('Channel is already on notify list. Use !stop_notify to remove channel from notify list.')
    else:
        # Else, add the channel to the dictionary, save the dictionary, and say when finished
        notify_channels.append(ctx.channel.id)
        save_channels()
        await ctx.send('Channel added to notify list.')


@bot.command(name='stop_notify', help='Removes the channel this command was used in from the notify list')
async def stop_notify(ctx):
    # Check if the channel is in the notify list in the first place
    if ctx.channel.id in notify_channels:
        notify_channels.remove(ctx.channel.id)

        # After appropriate things are removed, save channels and inform the user of completion
        save_channels()
        await ctx.send('Channel removed from the notify list.')
    else:
        # If channel is not on the list, say as much
        await ctx.send('Channel is not on the notify list. Use !notify to add it to the list.')


# Before starting the bot, load the current list of saved channels for notifications
notify_channels = load_channels()

# Start the bot and a second process for the stock checker
if __name__ == '__main__':

    product_check = threading.Thread(target=asyncio.run, args=(check_for_stock(),))
    product_check.start()

    bot.run(TOKEN)

    # Set bot_running to false so that way the check_for_stock function knows to exit its otherwise infinite loop
    bot_running = False

    product_check.join()
