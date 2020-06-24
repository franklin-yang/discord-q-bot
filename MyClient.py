import discord
import logging
from discord.ext import commands
import functools
from datetime import datetime, date, time
MAX_QUEUE_SIZE = 5;

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()
description = '''q bot'''
bot = commands.Bot(command_prefix='?', description=description)
from discord.ext import commands
bot = commands.Bot(command_prefix='$')
class Queue:
    members: set = set()
    time:datetime = None
    waitlist: set = set()

    def __init__(self, creator:commands.Context.author, time=datetime.now().time()):
        self.members.add(creator)
        self.time = time
    def get_q_members(self):
        return {functools.reduce(lambda acc, ele : f'{ele.name}\n{acc}', curr_q.members )}

curr_q : Queue= None

@bot.command()
async def foo(ctx, arg):
    await ctx.send(arg)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')



@bot.command()
async def newq(ctx:commands.Context, time_str:str):
    global curr_q
    try:
        if curr_q is None:
            q_time = datetime.strptime(time_str, '%H:%M%p').time()
            curr_q = Queue(ctx.message.author, q_time)
            await ctx.send(f'''
                            Q @ {q_time}
                            See you soon,
                            {curr_q.get_q_members()}
                            who's in?''')
    except Exception as e:
        print(e)

@bot.command()
async def moveq(ctx:commands.Context, time_str:str):
    global curr_q
    try:
        if curr_q is not None:
            q_time = datetime.strptime(time_str, '%H:%M%p').time()
            curr_q = Queue(ctx.message.author, q_time)
            await ctx.send(f'''
                            Heads up, q has been moved to {q_time}
                            See you then,
                            {curr_q.get_q_members()}''')
    except Exception as e:
        print(e)

@bot.command()
async def joinq(ctx:commands.Context):
    global curr_q
    try:
        if curr_q is not None and len(curr_q.members) < MAX_QUEUE_SIZE:
            await ctx.send(f"{ctx.message.author} joined \n \n{curr_q.get_q_members()}\n for a Q @ {curr_q.time} who else wants in?")
            curr_q.members.add(ctx.message.author)
    except Exception as e:
        print(e)

@bot.command()
async def clearq(ctx):
    try:
        global curr_q
        curr_q.members.clear()
        await ctx.send(f"q created for {curr_q.time} who's in?")
    except Exception as e:
        print(e)

@bot.event
async def on_reaction_add(reaction, user):
    global curr_q
    if len(curr_q.members) < MAX_QUEUE_SIZE:
        await reaction.message.channel.send(f"{user} joined \n \n{curr_q.get_q_members()}\n for a Q @ {curr_q.time} who else wants in?")
        curr_q.members.add(user)

def members_in_csgo_vc():
    channel = bot.get_channel(697674781058662401)
    cur_members = []
    for member in channel.members:
        cur_members.append(member)
    return cur_members

bot.run('NzI1MTMwMjIxOTg0MTUzNzEw.XvKQSg.Fas-xeMi6M2gtZJpu944GZ5PjVE')