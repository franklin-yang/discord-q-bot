import logging
from discord.ext import commands
from discord import abc, Message
from typing import Set, Optional
from datetime import datetime, time
from myToken import TOKEN

MAX_QUEUE_SIZE = 5

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

description = '''q bot'''
bot = commands.Bot(command_prefix='$')


class Queue:
    members: Set[abc.User] = set()
    wait_list: Set[abc.User] = set()
    time: time = None

    def __init__(self, creator: commands.Context.author, time: time = datetime.now().time()):
        self.members.add(creator)
        self.time = time

    @staticmethod
    def get_user_list_str(user_list:Set[abc.User]):
        return "\n".join(list(map(lambda x: x.name, user_list)))

    def get_q_member_mentions(self):
        return "\n".join(list(map(lambda x: x.mention, self.members)))

    def get_q_status(self):
        return f'\n__**Q Time:**__\n{self.time.strftime("%I:%M%p")}\
            \n__**On Deck:**__\n{self.get_user_list_str(self.members)}\n__**On Standby:**__\
            \n{self.get_user_list_str(self.wait_list)}'


curr_q : Optional[Queue] = None
last_message_sent: Optional[Message] = None
join_on_reac_msg: Optional[Message] = None


def parse_time(time_str: str):
    parsed_time = None
    for format_str in ['%I%p', '%I:%M%p']:
        try:
            parsed_time = datetime.strptime(time_str, format_str).time()
        except:
            pass
    return parsed_time



async def send_msg(ctx: commands.Context, msg_content: Optional[str], remove_prev=True):
    global last_message_sent
    sent = None
    if msg_content is not None:
        sent = await ctx.send(msg_content)
    if remove_prev and last_message_sent is not None:
        await last_message_sent.delete()
    if msg_content is not None:
        last_message_sent = sent
    return sent


@bot.command()
async def newq(ctx: commands.Context, time_str: str):
    global curr_q, join_on_reac_msg
    try:
        if curr_q is None:
            curr_q = Queue(ctx.message.author, parse_time(time_str))
            join_on_reac_msg = await send_msg(
                ctx,
                f'{ctx.message.author.name} has joined the Q!\n{curr_q.get_q_status()}'
            )
        else:
            await send_msg(
                ctx,
                f'\nThere is already a Q @ {curr_q.time.strftime("%I:%M%p")}\
                \nWould you like to move it?',
                False
            )
    except Exception as e:
        print(e)


@bot.command()
async def wl(ctx: commands.Context):
    global curr_q
    try:
        if curr_q is None:
            await ctx.send(f'There is no Q, would you like to create one with $newq HH:MM:PM?')
        else:
            if not (ctx.message.author in curr_q.wait_list):
                curr_q.members.discard(ctx.message.author)
                curr_q.wait_list.add(ctx.message.author)
            await send_msg(
                ctx,
                curr_q.get_q_status()
            )
    except Exception as e:
        print(e)


@bot.command()
async def hax(ctx: commands.Context):
    global curr_q
    try:
        await ctx.send('ekatana stop hacking')
    except Exception as e:
        print(e)


@bot.command()
async def m(ctx:commands.Context, time_str: str):
    global curr_q
    try:
        if curr_q is not None:
            curr_q.time = parse_time(time_str)
            await send_msg(
                ctx,
                f'\nQ has been moved to {curr_q.time.strftime("%I:%M%p")}!\n\
                Please react to this message to show that you are aware of the new time!\n\
                {curr_q.get_q_status()}'
            )
    except Exception as e:
        print(e)


@bot.command()
async def j(ctx:commands.Context):
    global curr_q
    try:
        if curr_q is not None and len(curr_q.members) < MAX_QUEUE_SIZE:
            curr_q.members.add(ctx.message.author)
            curr_q.wait_list.discard(ctx.message.author)
            await send_msg(
                ctx,
                f'\n{ctx.message.author.name} has joined the Q!\n\
                Please react to this message to show that you are aware of the new time!\n\
                {curr_q.get_q_status()}'
            )
    except Exception as e:
        print(e)


@bot.command()
async def clearq(ctx):
    try:
        global curr_q, last_message_sent
        curr_q = None

    except Exception as e:
        print(e)


@bot.command()
async def l(ctx: commands.Context):
    global curr_q
    if curr_q is not None:
        curr_q.members.discard(ctx.message.author)
        curr_q.wait_list.discard(ctx.message.author)
    await send_msg(
        ctx,
        f"looking for {5-len(curr_q.members)} more to join!\n{curr_q.get_q_status()}"
    )


@bot.event
async def on_reaction_add(reaction, user):
    global curr_q, last_message_sent
    if not curr_q is None and len(curr_q.members) < MAX_QUEUE_SIZE and join_on_reac_msg.id == reaction.message.id:
        await reaction.message.channel.send(f"{user} joined \n{curr_q.get_q_status()} who else wants in?")
        curr_q.members.add(user)


def members_in_csgo_vc():
    channel = bot.get_channel(697674781058662401)
    cur_members = []
    for member in channel.members:
        cur_members.append(member)
    return cur_members

bot.run(TOKEN)
