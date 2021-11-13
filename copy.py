import random
from datetime import datetime, time

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='#')

server_name = "凤凰堂"
address = [] # eth address

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print(bot.users)
    print('------')
    # for guild in bot.guilds:
    # if guild.name == server_name:
    #     for member in guild.members:
    #         print("Member:"+str(member))
    #     break
    # channel = await bot.fetch_channel('696193911332405321')
    # print(channel)
    # messages = await channel.history().flatten()
    # print("Here Are all messages:\n")
    # print(messages)
    # for guild in bot.guilds:
    #     for channel in guild.channels:
    #         print("Channel:"+str(channel))
    # for guild in bot.guilds:
    #     for member in guild.members:
    #         print("Member:"+str(member))

    # members = '\n - '.join([member.name for member in guild.members])
    # print(f'Guild Members:\n - {members}')


@bot.command()
async def delete_message(ctx):
    channel = bot.get_channel(696193911332405321)
    messages = await channel.history(limit=50).flatten()
    for message in messages:
        await message.delete()
        print("The content of message is:" + message.content)

    print("Work COMPLETED")

@bot.command()
async def get_members(ctx):
    embed = discord.Embed(
        title='Total Member:',
        description=f'There are currently **{ctx.guild.member_count}** members in the server!',
        timestamp=datetime.now(),
        color=discord.Colour.random()
    )
    embed.set_footer(text=f'{ctx.message.guild.name}')
    channel = bot.get_channel(696193911332405321)
    messages = await channel.history(limit=10).flatten()
    for message in messages:
        print("The content of message is:" + message.content)
    await ctx.send(f"{random.choice(messages).content}")


@bot.command()
async def info(ctx):
    print(ctx)
    embed = discord.Embed(title="WHO WHO WHO BOT", description="A bot", color=0xeee657)
    # give info about you here
    embed.add_field(name="Author", value="mr.spoon")
    # Shows the number of servers the bot is member of.
    embed.add_field(name="Server count", value=f"{len(bot.guilds)}")
    # give users a link to invite thsi bot to their server
    # embed.add_field(name="Invite", value="[Invite link](<insert your OAuth invitation link here>)")

    await ctx.send(embed=embed)


bot.remove_command('help')


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="nice bot", description="A Very Nice bot. List of commands are:", color=0xeee657)
    embed.add_field(name="#info", value="return info", inline=False)
    embed.add_field(name="#help", value="help menu", inline=False)
    embed.add_field(name="#delete_message", value="Will delete 200 messages in this channel.", inline=False)
    embed.add_field(name="#get_members", value="return member #", inline=False)
    await ctx.send(embed=embed)


bot.run('NzkzNzE0MTI1NzQ2MDc3NzI2.X-wR4g.CkN0RfFBPBrxgCEbYRK185SR4nU')
