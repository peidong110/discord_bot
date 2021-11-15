from discord.ext import commands
import helper as helper
import discord

bot = commands.Bot(command_prefix="#")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@commands.command(description="A method that delete 50 messages in the channel where the message command was sent.",brief="DELETE_MESSAGE METHOD")
async def delete_message(ctx):
    messages = await ctx.channel.history(limit=50).flatten()
    for message in messages:
        await message.delete()
        print("The content of message is:" + message.content)
    print("Work COMPLETED")
@commands.command(description="A method that will show stats of a miner in ethermine.",brief="SHOW MINER STATS")
async def add_miner(ctx,*args):
    
    if len(args) > 1:
        await ctx.channel.send(f'Sorry, you only need to put your address. Your current number of arguments is {len(args)} Prompt a Help command')
        # check if it's an valid address
    print(args)
    # await ctx.channel.send(args)
    address = args[0]
    is_address_valid = helper.is_valid_address(address)
    if is_address_valid:
        dic = helper.get_data(address)
        embed = discord.Embed(title="Miner Stats: ", color=0xeee657)
        for item in dic:
            embed.add_field(name=f'{item}', value=f'{dic[item]}')
        await ctx.channel.send(embed=embed)

bot.add_command(add_miner)
bot.add_command(delete_message)

bot.run('TOKEN')
