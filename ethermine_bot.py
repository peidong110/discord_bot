import time

import discord
import requests
from web3 import Web3, EthereumTesterProvider
# import asyncio
from discord.ext import commands

bot = commands.Bot(command_prefix='$')
end_point = "https://api.ethermine.org"
listening_flg = False
original_worker_lis = {}


def check_offline_worker(cur_workers, register_workers):
    # Input: list of workers, list of workers when registered
    # list of off-line worker
    # Constraints: This function will be only called when # of workers < registered workers.
    offline_worker = []
    for worker in register_workers:
        if worker not in cur_workers:
            offline_worker.append(worker)

    return offline_worker


def retrieve_original_worker(endpoint):
    initial_worker = []

    res = requests.get(url=endpoint)
    if res.status_code == 200:
        data = res.json()['data']
        for i in data:
            initial_worker.append(i)
    return initial_worker


def retrieve_current_worker(endpoint):
    cur_worker = []
    res = requests.get(url=endpoint)
    if res.status_code == 200:
        data = res.json()['data']
        for i in data:
            cur_worker.append(i)
    return cur_worker


async def register_miner(ctx, address, endpoint):
    if address in original_worker_lis:
        await ctx.channel.send("Address is already in the list")
    else:
        original = retrieve_original_worker(endpoint=endpoint)
        original_worker_lis[address] = original
        print("Miner Registered!")
        print(original_worker_lis)


async def start_listening(ctx):
    if len(original_worker_lis) < 1:
        await ctx.channel.send("You need to at least have one valid erc-20 registered")
    else:
        # If we have one address:
        for key in list(original_worker_lis):
            # miners.append(end_point + "/miner/" + args[0] + "/workers")
            current_worker = retrieve_current_worker(f"{end_point}/miner/{key}/workers")
            result = check_offline_worker(cur_workers=current_worker, register_workers=original_worker_lis[key])
            if len(result) > 1:
                await ctx.channel.send(f"{result} in {key}")
            else:
                await ctx.channel.send(f"Nothing Happened")


@commands.command(brief="start")
async def start(ctx):
    await ctx.channel.send("START!")
    while True:
        await start_listening(ctx=ctx)
        time.sleep(10)


@commands.command(brief="stop")
async def stop(ctx):
    global listening_flg
    listening_flg = False
    await ctx.channel.send("STOPPED!")


@commands.command(brief="add_miner")
async def add_address(ctx, *args):
    if len(args) == 1:
        # if argument is correct then validate address.
        if Web3.isAddress(args[0]):
            # if it's an erc20 address
            await register_miner(ctx, args[0], f"{end_point}/miner/{args[0]}/workers")

            # await start_listening(ctx=ctx)
        else:
            await ctx.channel.send(f'Sorry, address format is wrong')


async def message_box(title, message, ctx):
    if title == "Succeeded":
        embed = discord.Embed(title=f'{title}: ', color=discord.colour.Color.green())
    elif title == "Reason":
        embed = discord.Embed(title=f'{title}: ', color=discord.colour.Color.red())
    else:
        embed = discord.Embed(title=f'{title}: ', color=discord.colour.Color.random())

    embed.add_field(name="MSG", value=f'{message}')
    await ctx.channel.send(embed=embed)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    for guild in bot.guilds:
        print(guild)


#
# @bot.event
# async def on_message(message):

@bot.event
async def on_message(msg):
    # do some extra stuff here
    await bot.process_commands(msg)
    if msg.author == bot.user:
        return
    # if msg.content.startswith('Hello World'):
    # await msg.channel.send('Hell World')
    ctx = await bot.get_context(msg)
    member = msg.author
    word_in_banned_list = any(word in msg.content for word in banned_item_list)
    if word_in_banned_list:
        await member.kick(reason='YOU Entered BAD WORD')
        await ctx.channel.send(f"{msg.author.mention} was kicked")
        await message_box("Reason", f"Forbidden Message Detected:\n {msg.content}", ctx)
        await msg.delete()
        print(f"{msg.author} was kicked")
    # else:
    # print(msg.content)


bot.add_command(add_address)
bot.add_command(start)
bot.add_command(stop)

bot.run('TOKEN')
