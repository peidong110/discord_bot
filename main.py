from discord.ext import commands
import helper as helper
import discord

bot = commands.Bot(command_prefix="$")
addresses = []


async def message_box(title, message, ctx):
    if title == "Succeeded":
        embed = discord.Embed(title=f'{title}: ', color=discord.colour.Color.green())
    elif title == "Failed":
        embed = discord.Embed(title=f'{title}: ', color=discord.colour.Color.red())
    else:
        embed = discord.Embed(title=f'{title}: ', color=discord.colour.Color.random())

    embed.add_field(name="MSG", value=f'{message}')
    await ctx.channel.send(embed=embed)


async def show_stats(ctx):
    embed = discord.Embed(title="Miner Stats: ", color=0xeee657)
    for address in addresses:
        dic = helper.get_data(address)
        for i in dic:
            embed.add_field(name=f'{i}', value=f'{dic[i]}')
        await ctx.channel.send(embed=embed)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@commands.command(description="A method that delete 50 messages in the channel where the message command was sent.",
                  brief="Deletes messages in a channel.")
async def delete_message(ctx):

    messages = await ctx.channel.history(limit=50).flatten()
    for message in messages:
        await message.delete()
        print("The content of message is:" + message.content)

    print("Work COMPLETED")
    await message_box("Congratulations", f"You just delete {len(messages)} message in this channel", ctx)


@commands.command(description="A method that will add stats of a miner in ethermine.", brief="Adds miner")
async def add_miner(ctx, *args):
    if len(args) > 1:
        await ctx.channel.send(
            f'Sorry, you only need to put your address. Your current number of arguments is {len(args)} Prompt a Help command')
        # check if it's an valid address

    # await ctx.channel.send(args)
    author_name = ctx.author.name
    address = args[0]
    is_address_valid = helper.is_valid_address(address)
    if is_address_valid and address not in addresses:
        addresses.append(address)
        await message_box("Succeeded", f"Hi {author_name},\n You just successfully added a miner.", ctx)
    else:
        await message_box("Failed", f"Hi {author_name},\n  The address you just entered is either wrong or already in the list.", ctx)


@commands.command(description="A method that will show miner stats in ethermine pool.", brief="Shows miner stats")
async def show_miner_stats(ctx):
    if len(addresses) < 0:
        await ctx.channel.send("HEY, You haven't add a miner yet!")
    else:
        await show_stats(ctx)


bot.add_command(add_miner)
bot.add_command(delete_message)
bot.add_command(show_miner_stats)
bot.run('TOKEN')
