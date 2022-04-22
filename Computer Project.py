#######################################################################################################################

import asyncio
import csv
import datetime
import random
import textwrap

import aiohttp
import discord  # this is used for interacting with the discord API
import discord.utils
from PIL import Image  # Used for image file handling
from PIL import ImageDraw
from PIL import ImageFont
from discord import Member
from discord import Webhook, AsyncWebhookAdapter
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.ext.commands import MissingRequiredArgument
# Used for programming buttons to work with discord along with slash commands
from discord_components import DiscordComponents, Button, ButtonStyle
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice
from googlesearch import search  # This is the module that makes the gsearch command possible

#######################################################################################################################
file = open("Setup.csv", "r")
row = list(csv.reader(file))[1:]
file.close()
if not row:
    print("This is the initial setup for the bot, you can change these details in the Setup.csv file. You will only "
          "have to do this once")
    file = open("Setup.csv", "w", newline="")
    writer = csv.writer(file)
    writer.writerow(["Owner_id", "Guild_ids", "bot_token"])
    owner_id = int(input("Enter your discord ID: "))
    guild_ids = eval(input("Enter the guild ids of your bot in the form of a list (for slash commands): "))
    bot_token = input("Enter your discord bot token: ")
    writer.writerow([owner_id, guild_ids, bot_token])
    file.close()
else:
    row = row[0]
    owner_id = int(row[0])
    guild_ids = eval(row[1])
    bot_token = row[2]
# Initiating leaderboard
'''file = open("Leaderboard.csv", "w", newline="")
writer = csv.writer(file)
writer.writerow(["ID", "Score"])
file.close()'''

'''points:
win: +10
tie: 0
lose: -10'''

# Updating leaderboard scored based on user ID
def Score(u_id, points):
    file = open("Leaderboard.csv", "r")
    rows = list(csv.reader(file))[1:]
    file.close()
    for row in rows:
        try:
            if int(row[0]) == int(u_id):
                row[1] = points + int(row[1])
                break
        except:
            pass
    else:
        rows.append([u_id, points])
    file = open("Leaderboard.csv", "w", newline="")
    writer = csv.writer(file)
    writer.writerow(["ID", "Score"])
    writer.writerows(rows)
    if points > 0:
        print(f"{u_id} won {points} points")
    elif points < 0:
        print(f"{u_id} lost {abs(points)} points")
    else:
        print(f"{u_id} got no points")


# Concatenating *args to simple strings for awkward discord functions
def fix(lst):
    string = ""
    for i in lst:
        string += i + " "
    return string[:-1]

# Converts the image into a clean circle
def circular(img, size_x=256, size_y=256):
    img = img.resize((size_x, size_y))
    big_size = (img.size[0] * 3, img.size[1] * 3)
    mask = Image.new('L', big_size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + big_size, fill=255)
    mask = mask.resize(img.size, Image.ANTIALIAS)
    img.putalpha(mask)
    return img


# This is the description of the bot and here, the prefix is defined
description = '''Multipurpose Discord Bot'''
bot = commands.Bot(command_prefix='?', description=description)
bot.remove_command('help')
slash = SlashCommand(bot, sync_commands=True)
DiscordComponents(bot)


# @bot.event refers to those events that happen automatically without being invoked by a user
#######################################################################################################################

# This block of code is executed when the bot starts up
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------------------')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="out for ?bothelp"))


#######################################################################################################################

# This block of code handles errors that arise when command is not found
@bot.event
async def on_command_error(ctx, error):
    if str(error) == 'command is a required argument that is missing.':
        return
    elif isinstance(error, MissingRequiredArgument):
        await ctx.send(str(error))
        return
    elif isinstance(error, commands.UnexpectedQuoteError):
        return
    elif isinstance(error, CommandNotFound):
        await ctx.send(str(error))
        return
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(str(error))
        return
    else:
        await ctx.send(str(error))
    raise error


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""@bot.command are commands that are invoked by a user when they type some pre-defined text with the above defined
prefix """


#######################################################################################################################

# This is the help command. It allows the user to get more information about each command
@bot.command()
async def bothelp(ctx, command):
    command = str(command).lower()
    await ctx.message.delete()

    if command == "clean":
        embed = discord.Embed(title="?clean [message_count]", timestamp=datetime.datetime.utcnow(),
                              description="Deletes all messages in the given "
                                          "limit (admin only)", color=discord.Color.teal())
        embed.set_author(name="Requested by " + ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    elif command == "bothelp":
        embed = discord.Embed(title="?bothelp", timestamp=datetime.datetime.utcnow(),
                              description="If you managed to see this, I think you know what you are doing. "
                                          "Anyways, use ?botlist to get a list of commands", color=discord.Color.teal())
        embed.set_author(name="Requested by " + ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    elif command == "sps":
        embed = discord.Embed(title="?sps", timestamp=datetime.datetime.utcnow(),
                              description="Play Stone paper scissors "
                                          "with the bot", color=discord.Color.teal())
        embed.set_author(name="Requested by " + ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    elif command == "gsearch":
        embed = discord.Embed(title="/gsearch [query]", timestamp=datetime.datetime.utcnow(),
                              description="Returns the first 3 Google results for given query",
                              color=discord.Color.teal())
        embed.set_author(name="Requested by " + ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    elif command == "ping":
        embed = discord.Embed(title="/ping", timestamp=datetime.datetime.utcnow(),
                              description="Returns the ping time for the bot",
                              color=discord.Color.teal())
        embed.set_author(name="Requested by " + ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    elif command == "flip":
        embed = discord.Embed(title="/flip [choice]", timestamp=datetime.datetime.utcnow(),
                              description="A coin flipping game using discord slash commands",
                              color=discord.Color.teal())
        embed.set_author(name="Requested by " + ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    elif command == "ttt":
        embed = discord.Embed(title="?ttt @member_name", timestamp=datetime.datetime.utcnow(),
                              description="With this command, you can play tic tac toe with another user from the "
                                          "server by tagging their name while calling the command",
                              color=discord.Color.teal())
        embed.set_author(name="Requested by " + ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    elif command == "botlist":
        embed = discord.Embed(title="?botlist", timestamp=datetime.datetime.utcnow(),
                              description="This is the command used to get the list of all commands that the bot "
                                          "currently supports",
                              color=discord.Color.teal())
        embed.set_author(name="Requested by " + ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    elif command == "tzu":
        embed = discord.Embed(title="/tzu [quote]", timestamp=datetime.datetime.utcnow(),
                              description="Quote from Chinese strategist Sun Tzu, author of \"The Art of War\"",
                              color=discord.Color.teal())
        embed.set_image(url="https://media.discordapp.net/attachments/785820735246827530/796353995853529128/image1.png")
        embed.set_author(name="Requested by " + ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    elif command == "say":
        embed = discord.Embed(title="/say @member_name", timestamp=datetime.datetime.utcnow(),
                              description="Ever wanted to put words in someone else's mouth? Well now you can.",
                              color=discord.Color.teal())
        embed.set_author(name="Requested by " + ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    elif command == "calculator":
        embed = discord.Embed(title="?calculator", timestamp=datetime.datetime.utcnow(),
                              description="A fully functioning calculator programmed using discord components",
                              color=discord.Color.teal())
        embed.set_author(name="Requested by " + ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    elif command == "image":
        embed = discord.Embed(title="/image", timestamp=datetime.datetime.utcnow(),
                              description="Demonstration of Image file handling using the PIL package",
                              color=discord.Color.teal())
        embed.set_author(name="Requested by " + ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    elif command == "leaderboard":
        embed = discord.Embed(title="/leaderboard", timestamp=datetime.datetime.utcnow(),
                              description="Displays all the leaderboard rankings",
                              color=discord.Color.teal())
        embed.set_author(name="Requested by " + ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    elif command == "click":
        embed = discord.Embed(title="?click", timestamp=datetime.datetime.utcnow(),
                              description="A simple game with new discord components. First person to click the button"
                                          " wins. The button will show up after some random time so you have to be "
                                          "careful.",
                              color=discord.Color.teal())
        embed.set_author(name="Requested by " + ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    else:
        title = "Command \"" + command + "\" not found"
        embed = discord.Embed(title=title, timestamp=datetime.datetime.utcnow(),
                              description="To get a list of all available commands, type: ```?botlist```",
                              color=discord.Color.teal())
        embed.set_author(name="Requested by " + ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


# This block of code handles errors caused due to improper use of bothelp command
@bothelp.error
async def bothelp_error(ctx, error):
    embed = discord.Embed(title="To use ?bothelp, type:", timestamp=datetime.datetime.utcnow(),
                          description="```?bothelp [command name]```",
                          color=discord.Color.teal())
    embed.add_field(name="To get a list of all commands, type: ", value="```?botlist```", inline=False)
    text = "Also try out slash commands!"
    embed.set_footer(text=text)
    await ctx.send(embed=embed)


#######################################################################################################################

# This is the list command used to get a list of commands the bot can perform
@bot.command()
async def botlist(ctx):
    await ctx.message.delete()

    page1 = discord.Embed(title="Commands list", timestamp=datetime.datetime.utcnow(),
                          description="Name of command and format",
                          color=discord.Color.light_grey())
    page1.set_author(name="Requested by " + ctx.author.display_name, icon_url=ctx.author.avatar_url)
    page1.add_field(name="List", value="```?botlist```", inline=False)
    page1.add_field(name="Bothelp", value="```?bothelp [command]```", inline=False)
    page1.add_field(name="Calculate", value="```?calculator```", inline=False)
    page1.add_field(name="Click", value="```?click```", inline=False)
    page1.add_field(name="Stone Paper Scissors", value="```?sps```", inline=False)
    page1.add_field(name="Tic Tac Toe", value="```?ttt @member_name```", inline=False)
    page1.add_field(name="Clean", value="```?clean [message_count]```", inline=False)
    page1.set_footer(text="1/2")

    page2 = discord.Embed(title="Commands list ", timestamp=datetime.datetime.utcnow(),
                          description="Name of command and format",
                          color=discord.Color.light_grey())
    page2.set_author(name="Requested by " + ctx.author.display_name, icon_url=ctx.author.avatar_url)
    page2.add_field(name="Sun tzu", value="```/tzu [quote]```", inline=False)
    page2.add_field(name="Say", value="```/say @member_name```", inline=False)
    page2.add_field(name="Leaderboard", value="```/leaderboard```", inline=False)
    page2.add_field(name="Coin flip", value="```/flip [side]```", inline=False)
    page2.add_field(name="Google Search", value="```/gsearch [query]```", inline=False)
    page2.add_field(name="Ping", value="```/ping```", inline=False)
    page2.add_field(name="Image", value="```/image```", inline=False)
    page2.set_footer(text="2/2")

    pages = [page1, page2]

    message = await ctx.send(embed=page1)
    await message.add_reaction('◀')
    await message.add_reaction('▶')

    def check(rxn, usr):
        return usr == ctx.author

    i = 0
    reaction = None

    while True:
        if str(reaction) == '◀':
            if i > 0:
                i -= 1
                await message.edit(embed=pages[i])
        elif str(reaction) == '▶':
            if i < 1:
                i += 1
                await message.edit(embed=pages[i])

        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
            await message.remove_reaction(reaction, user)
        except:
            break

    await message.clear_reactions()


#######################################################################################################################

# This command is used for bulk deleting the messages in a channel
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clean(ctx, limit: int):
    try:
        await ctx.channel.purge(limit=limit)
        await ctx.message.delete()
    except:
        return
#######################################################################################################################
# Get the guild_id for setup and maintenance
@bot.command()
async def guild_id(ctx):
    await ctx.send(ctx.guild.id)


#######################################################################################################################

# Play stone paper scissors against the bot
@bot.command()
async def sps(ctx):
    emojis = ['✊', '✋', '✂']
    embed = discord.Embed(title="Select your option by reacting below", color=discord.Color.blurple())
    message = await ctx.send(embed=embed)

    for Emoji in emojis:
        await message.add_reaction(Emoji)

    rand = random.randint(1, 3)
    win = discord.Embed(title="Congratulations, You Won!", color=discord.Color.gold())
    tie = discord.Embed(title="It was a tie!", color=discord.Color.gold())
    loss = discord.Embed(title="Oh no! You lost.", color=discord.Color.gold())

    def check(rxn, usr):
        return usr == ctx.author

    switch = 1
    reaction = None

    while True:
        if str(reaction) == '✊':
            if rand == 3:
                await ctx.send(embed=win)
                Score(ctx.author.id, 10)
            elif rand == 2:
                await ctx.send(embed=tie)
                Score(ctx.author.id, 0)
            else:
                await ctx.send(embed=loss)
                Score(ctx.author.id, -10)
        elif str(reaction) == '✋':
            if rand == 1:
                await ctx.send(embed=win)
                Score(ctx.author.id, 10)
            elif rand == 3:
                await ctx.send(embed=tie)
                Score(ctx.author.id, 0)
            else:
                await ctx.send(embed=loss)
                Score(ctx.author.id, -10)
        elif str(reaction) == '✂':
            if rand == 2:
                await ctx.send(embed=win)
                Score(ctx.author.id, 10)
            elif rand == 1:
                await ctx.send(embed=tie)
                Score(ctx.author.id, 0)
            else:
                await ctx.send(embed=loss)
                Score(ctx.author.id, -10)
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
            if switch == 1:
                switch = 0
                continue
            elif switch == 0:
                break

        except:
            break

    await message.clear_reactions()


#######################################################################################################################

# This is the tic-tac-toe command which allows someone to play a game of tic-tac-toe with another user from the server
'''X -> Player who initiated (ctx)
Y-> Player_2'''


@bot.command()
async def ttt(ctx, Player_2: Member):
    b = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    game_over = False
    player = "X"
    # This is the board command responsible for printing the board for the game
    board = f'''```
      |     |
   {b[0]}  |  {b[1]}  |  {b[2]}
 _____|_____|_____
      |     |
   {b[3]}  |  {b[4]}  |  {b[5]}
 _____|_____|_____
      |     |
   {b[6]}  |  {b[7]}  |  {b[8]}
      |     |
```'''
    embed = discord.Embed(title="Below is the format of the tic tac toe board",
                          description=ctx.author.display_name + "'s turn to play (X) \n" + board,
                          color=discord.Color.blue())
    await ctx.send(embed=embed)
    b = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    avail_space = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    count = 0

    def check(m):
        if count % 2 == 0:
            return m.author == ctx.author and m.channel == ctx.channel
        else:
            return m.author == Player_2 and m.channel == ctx.channel

    while not game_over:
        embed = discord.Embed(title="Type a position from " + str(avail_space), color=discord.Color.blue())
        await ctx.send(embed=embed)
        try:
            msg = await bot.wait_for('message', check=check, timeout=15)
            try:
                user_input = int(msg.content)
                if user_input in avail_space:
                    b[int(user_input - 1)] = player
                    board = f'''```
      |     |
   {b[0]}  |  {b[1]}  |  {b[2]}
 _____|_____|_____
      |     |
   {b[3]}  |  {b[4]}  |  {b[5]}
 _____|_____|_____
      |     |
   {b[6]}  |  {b[7]}  |  {b[8]}
      |     |
```'''
                    if count % 2 == 0:
                        title = Player_2.display_name + "'s turn to play (O)"
                    else:
                        title = ctx.author.display_name + "'s turn to play (X)"
                    embed = discord.Embed(title=title,
                                          description=board,
                                          color=discord.Color.blue())
                    await ctx.send(embed=embed)
                    try:
                        avail_space.remove(user_input)
                        count += 1
                    except:
                        continue
                    if count % 2 == 0:
                        player = "X"
                    else:
                        player = "O"
                else:
                    embed = discord.Embed(title="Please pick a position from the available options.",
                                          color=discord.Color.red())
                    await ctx.send(embed=embed)
                    continue
                # Checking for win condition
                if b[0] == b[1] == b[2] != " ":
                    if b[0] == "X":
                        Score(ctx.author.id, +10)
                        Score(Player_2.id, -10)
                    else:
                        Score(Player_2.id, +10)
                        Score(ctx.author.id, -10)
                    embed = discord.Embed(title=f"{b[0]} has won the game!",
                                          color=discord.Color.gold())
                    await ctx.send(embed=embed)
                    game_over = True

                elif b[3] == b[4] == b[5] != " ":
                    if b[3] == "X":
                        Score(ctx.author.id, +10)
                        Score(Player_2.id, -10)
                    else:
                        Score(Player_2.id, +10)
                        Score(ctx.author.id, -10)
                    embed = discord.Embed(title=f"{b[3]} has won the game!",
                                          color=discord.Color.gold())
                    await ctx.send(embed=embed)
                    game_over = True

                elif b[6] == b[7] == b[8] != " ":
                    if b[6] == "X":
                        Score(ctx.author.id, +10)
                        Score(Player_2.id, -10)
                    else:
                        Score(Player_2.id, +10)
                        Score(ctx.author.id, -10)
                    embed = discord.Embed(title=f"{b[6]} has won the game!",
                                          color=discord.Color.gold())
                    await ctx.send(embed=embed)
                    game_over = True

                elif b[0] == b[3] == b[6] != " ":
                    if b[0] == "X":
                        Score(ctx.author.id, +10)
                        Score(Player_2.id, -10)
                    else:
                        Score(Player_2.id, +10)
                        Score(ctx.author.id, -10)
                    embed = discord.Embed(title=f"{b[0]} has won the game!",
                                          color=discord.Color.gold())
                    await ctx.send(embed=embed)
                    game_over = True

                elif b[1] == b[4] == b[7] != " ":
                    if b[1] == "X":
                        Score(ctx.author.id, +10)
                        Score(Player_2.id, -10)
                    else:
                        Score(Player_2.id, +10)
                        Score(ctx.author.id, -10)
                    embed = discord.Embed(title=f"{b[1]} has won the game!",
                                          color=discord.Color.gold())
                    await ctx.send(embed=embed)
                    game_over = True

                elif b[2] == b[5] == b[8] != " ":
                    if b[2] == "X":
                        Score(ctx.author.id, +10)
                        Score(Player_2.id, -10)
                    else:
                        Score(Player_2.id, +10)
                        Score(ctx.author.id, -10)
                    embed = discord.Embed(title=f"{b[2]} has won the game!",
                                          color=discord.Color.gold())
                    await ctx.send(embed=embed)
                    game_over = True

                elif b[0] == b[4] == b[8] != " ":
                    if b[0] == "X":
                        Score(ctx.author.id, +10)
                        Score(Player_2.id, -10)
                    else:
                        Score(Player_2.id, +10)
                        Score(ctx.author.id, -10)
                    embed = discord.Embed(title=f"{b[0]} has won the game!",
                                          color=discord.Color.gold())
                    await ctx.send(embed=embed)
                    game_over = True

                elif b[2] == b[4] == b[6] != " ":
                    if b[2] == "X":
                        Score(ctx.author.id, +10)
                        Score(Player_2.id, -10)
                    else:
                        Score(Player_2.id, +10)
                        Score(ctx.author.id, -10)
                    embed = discord.Embed(title=f"{b[2]} has won the game!",
                                          color=discord.Color.gold())
                    await ctx.send(embed=embed)
                    game_over = True

                elif ' ' not in b:
                    embed = discord.Embed(title="The board is full and the game is a tie",
                                          color=discord.Color.dark_gold())
                    await ctx.send(embed=embed)
                    game_over = True

            except:
                embed = discord.Embed(title="Please pick a position from the available options.",
                                      color=discord.Color.red())
                await ctx.send(embed=embed)
        except asyncio.TimeoutError as e:
            embed = discord.Embed(title="Looks like you waited too long",
                                  description="Please restart the game to play again.",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)
            break


#######################################################################################################################
# Shutdown the bot physically in case of misbehaving
@bot.command()
async def shutdown(ctx):
    if ctx.author.id == owner_id:
        await ctx.send("Shutting down")
        quit()
    else:
        await ctx.send("You are not authorised to do this", delete_after=5)


#######################################################################################################################

'''This is where all the slash commands are written. It is an easier way to interact with the bot using discord's built-
in interface. Allows for more features and options'''


@slash.slash(name="ping", description="Get the ping time for this bot", guild_ids=guild_ids)
async def _ping(ctx):  # Defines a new "context" (ctx) command called "ping."
    lat = bot.latency * 1000
    lat = format(lat, ".3f")
    embed = discord.Embed(title=f"Pong! ({lat} ms)", color=discord.Color.gold())
    await ctx.send(embed=embed)


#######################################################################################################################

# Allows multiple types of inputs from the user using slash commands
@slash.slash(name="say",
             description="Ever wanted to put words in someone else's mouth? Well now you can",
             guild_ids=guild_ids,
             options=[create_option(name="user",
                                    description="Enter name of user to impersonate",
                                    option_type=6,
                                    required=True),
                      create_option(name="message",
                                    description="What do you want the user to say?",
                                    option_type=3,
                                    required=True),
                      create_option(name="channel",
                                    description="Channel where you want to send the message",
                                    option_type=7,
                                    required=False)
                      ])
async def _say(ctx, user: discord.user, message: str, channel: discord.TextChannel = None):
    if channel:
        try:
            webhook = await channel.create_webhook(name=user.display_name)
            await webhook.send(message, avatar_url=user.avatar_url)
            await webhook.delete()
        except:
            embed = discord.Embed(title="Please select a valid channel", color=discord.Color.red())
            await ctx.send(embed=embed, hidden=True)
            return
    else:
        try:
            webhook = await ctx.channel.create_webhook(name=user.display_name)
            await webhook.send(message, avatar_url=user.avatar_url)
            await webhook.delete()
        except:
            embed = discord.Embed(title="If you can see the message below then all is good otherwise this is an error.",
                                  color=discord.Color.red())
            await ctx.send(embed=embed, hidden=True)
            return
    embed = discord.Embed(title="Impersonation successful", color=discord.Color.gold())
    await ctx.send(embed=embed, hidden=True)


#######################################################################################################################
# Writing text on image using Image file handling
@slash.slash(name="tzu",
             description="Write a quote from the great strategist Sun Tzu",
             guild_ids=guild_ids,
             options=[
                 create_option(name="message",
                               description="Enter your quote",
                               option_type=3,
                               required=True)
             ])
async def _tzu(ctx, message: str):
    img = Image.open("sun.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("impact.ttf", 50)
    value = message
    wrapper = textwrap.TextWrapper(width=24)
    string = wrapper.fill(text=value)
    draw.text((200, 65), string, (255, 255, 255), font=font)
    img.save('image1.png')
    await ctx.reply(file=discord.File('image1.png'))

#######################################################################################################################
# gsearch command allows searching google for a given query and returns the result
@slash.slash(name="gsearch",
             description="Get google results from the comfort of discord",
             guild_ids=guild_ids,
             options=[
                 create_option(name="message",
                               description="Enter your query",
                               option_type=3,
                               required=True)
             ])
async def _gsearch(ctx, message: str):
    query = message
    embed = discord.Embed(title="Given query: ", description="```" + query + "```",
                          timestamp=datetime.datetime.utcnow(), color=discord.Color.greyple())
    embed.set_author(name="Requested by " + ctx.author.display_name, icon_url=ctx.author.avatar_url)
    await ctx.reply(embed=embed)
    count = 1
    async with ctx.channel.typing():
        for j in search(query):
            embed = discord.Embed(title="Result " + str(count), color=discord.Color.greyple())
            if count > 3:  # Number of results
                break
            count += 1
            await ctx.channel.send(embed=embed)
            await ctx.channel.send(j)
        await asyncio.sleep(1)


#######################################################################################################################
# command to print the leaderboard details from a csv file
@slash.slash(name="leaderboard", description="Display the current leaderboard", guild_ids=guild_ids)
async def _leaderboard(ctx):
    file = open("Leaderboard.csv", "r")
    rows = list(csv.reader(file))[1:]
    for row in rows:
        row[0] = await bot.fetch_user(int(row[0]))
        row[1] = int(row[1])
    rows.sort(key=lambda x: x[1], reverse=True)
    pos = 1
    for row in rows:
        embed = discord.Embed(title=f"Rank {pos}: {row[0].display_name}", color=discord.Color.gold())
        embed.add_field(name="Score", value=f"```{row[1]}```", inline=False)
        embed.set_thumbnail(url=row[0].avatar_url)
        await ctx.send(embed=embed)
        pos += 1


#######################################################################################################################
# Flipping a coin using a random variable
@slash.slash(name="flip",
             description="Flip a coin", guild_ids=guild_ids,
             options=[create_option(name="side",
                                    description="Pick the side you want",
                                    option_type=3,
                                    choices=[
                                        create_choice(
                                            name="Heads",
                                            value="Heads"
                                        ),
                                        create_choice(
                                            name="Tails",
                                            value="Tails"
                                        ),
                                    ],
                                    required=True)
                      ]
             )
async def _flip(ctx, side: str):
    import random
    msg = await ctx.send("https://tenor.com/view/coin-toss-coin-toss-gif-5017733")
    await asyncio.sleep(3)
    out = random.choice(["Heads", "Tails"])
    win = discord.Embed(title=f"Congratulations! it was {side}", color=discord.Color.gold())
    loss = discord.Embed(title=f"Oh no! it was {out}", color=discord.Color.gold())
    if out == side:
        Score(ctx.author.id, 10)
        await msg.edit(content="", embed=win)
    else:
        await msg.edit(content="", embed=loss)
        Score(ctx.author.id, -10)


#######################################################################################################################
# A simple command to demonstrate image file handling using PIL
@slash.slash(name="image",
             description="This command is used to show file handling using images in python",
             guild_ids=guild_ids,
             options=[create_option(name="user",
                                    description="Tag the user to use for the command",
                                    option_type=6,
                                    required=True)
                      ])
async def _image(ctx, user: discord.User):
    try:
        await user.avatar_url.save("avatar.png")
        avatar = Image.open("avatar.png").convert('RGB')
        avatar = circular(avatar, 375, 375)
        img = Image.open("welcome.jpg")
        img.paste(avatar, (495, 160), avatar)
        img.save('sample-out.jpg')
        await ctx.send(file=discord.File('sample-out.jpg'))
        return
    except:
        embed = discord.Embed(title="If you can see the message below then all is good otherwise this is an error.",
                              color=discord.Color.red())
        await ctx.send(embed=embed, hidden=True)
        return


#######################################################################################################################
# A simple button based game which tests reflexes and skill
@bot.command()
async def click(ctx):
    from random import randint
    await ctx.message.delete()
    embed = discord.Embed(title="The game has begun", color=discord.Colour.blurple())
    m = await ctx.send(embed=embed)
    num = randint(5, 10)
    await asyncio.sleep(num)
    await m.edit(
        embed=discord.Embed(title="Button waiting for a click", color=discord.Colour.teal()),
        components=[
            Button(style=ButtonStyle.blue, label="Click Me!"),
        ],
    )

    def check(response):
        return ctx.author == response.user and response.channel == ctx.channel

    try:
        res = await bot.wait_for("button_click", check=check, timeout=5)
        await res.respond(
            type=4, content="You Won!"
        )
        Score(ctx.author.id, +10)
        await m.edit(
            embed=discord.Embed(title=f"The winner is {res.user.display_name}", color=discord.Color.gold()),
            components=[
                Button(style=ButtonStyle.green, label="Winner decided!", disabled=True),
            ],
        )

    except:
        Score(ctx.author.id, -5)
        await m.edit(
            embed=discord.Embed(title="You took too long", color=discord.Color.red()),
            components=[
                Button(style=ButtonStyle.red, label="Timeout!", disabled=True),
            ],
        )


#######################################################################################################################
# A fully function calculator built into discord utilising multiple button arrays and inbuilt python expressions
@bot.event
async def on_button_click(interaction):
    pass


@bot.command()
async def calculator(ctx):
    exp = " "
    buttons = [
        [
            Button(style=ButtonStyle.blue, label="1", custom_id="1"),
            Button(style=ButtonStyle.blue, label="2", custom_id="2"),
            Button(style=ButtonStyle.blue, label="3", custom_id="3"),
            Button(style=ButtonStyle.green, label="+", custom_id="+"),
        ],
        [
            Button(style=ButtonStyle.blue, label="4", custom_id="4"),
            Button(style=ButtonStyle.blue, label="5", custom_id="5"),
            Button(style=ButtonStyle.blue, label="6", custom_id="6"),
            Button(style=ButtonStyle.green, label="-", custom_id="-"),
        ],
        [
            Button(style=ButtonStyle.blue, label="7", custom_id="7"),
            Button(style=ButtonStyle.blue, label="8", custom_id="8"),
            Button(style=ButtonStyle.blue, label="9", custom_id="9"),
            Button(style=ButtonStyle.green, label="*", custom_id="*"),
        ],
        [
            Button(style=ButtonStyle.blue, label=".", custom_id="."),
            Button(style=ButtonStyle.blue, label="0", custom_id="0"),
            Button(style=ButtonStyle.green, label="=", custom_id="="),
            Button(style=ButtonStyle.green, label=r"/", custom_id=r"/"),
        ],
        [
            Button(style=ButtonStyle.green, label="(", custom_id="("),
            Button(style=ButtonStyle.green, label=")", custom_id=")"),
            Button(style=ButtonStyle.green, label="exp", custom_id="**("),
            Button(style=ButtonStyle.red, label="C", custom_id="C"),
        ]
    ]
    m = await ctx.send(f"```{exp}```", components=buttons)

    def check(response):
        return ctx.author == response.user and response.channel == ctx.channel

    flag = False
    try:
        while True:
            if flag:
                exp = " "
                flag = False

            num = " "
            res = await bot.wait_for("button_click", check=check)
            num = str(res.custom_id)

            if num == "=":
                try:
                    exp = str(eval(exp))
                except:
                    exp = "ERROR"
                    flag = True

            elif num == "C":
                exp = " "

            else:
                exp += num

            await res.respond(type=6)
            await m.edit(f"```{exp}```", components=buttons)

    except:
        return


#######################################################################################################################
#######################################################################################################################
"""This is the bot token. This is a unique identification number that correlates to this particular bot only. This is
as important as a password since anyone with this token can take control of the bot. """

bot.run(bot_token)
