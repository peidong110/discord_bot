import discord
# import asyncio
from discord.ext import commands

bot = commands.Bot(command_prefix='-')
banned_item_list = ["如果你還不知道如何把握市場運行方向", "免費諮詢個股", "老師也會不定期進羣", "推薦一個不錯的美股交易羣", "羣裡會有好的股票推薦", "每週都會有10-30%以上的收入", "不收費",
                    "羣裡每天都會分享最新的行情諮詢", "不收費，不分工", "https://chat.whatsapp.com", "不收費，不分工", "推荐一个不错的美股", "推薦一個不錯",
                    "美股交易羣", "免费咨询个股"]


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
    # else:
        # print(msg.content)


bot.run('TOKEN')
