from discord.ext import commands
import helper as helper
import discord

bot = commands.Bot(command_prefix="$")
addresses = []
banned_item_list = set()

"""
This message_box() function, will console.log an embed with customized message to the channel where the msg was sent.
Input:
        Title-> the title of the message box (STRING)
        Message-> The message you want to pass in (STRING)
        ctx -> The context (CONTEXT Object)
command:
    message_box("Succeeded", "You have successfully added the item to the list",ctx)
"""


async def message_box(title, message, ctx):
    if title == "Succeeded":
        embed = discord.Embed(title=f'{title}: ', color=discord.colour.Color.green())
    elif title == "Failed":
        embed = discord.Embed(title=f'{title}: ', color=discord.colour.Color.red())
    else:
        embed = discord.Embed(title=f'{title}: ', color=discord.colour.Color.random())

    embed.add_field(name="MSG", value=f'{message}')
    await ctx.channel.send(embed=embed)


"""
This show_stats(ctx) function, will display the stats of a miner in the list.
Input:
        ctx -> The context (CONTEXT Object)
command:
    show_stats(ctx)
"""


async def show_stats(ctx):
    embed = discord.Embed(title="Miner Stats: ", color=0xeee657)
    for address in addresses:
        dic = helper.get_data(address)
        for i in dic:
            embed.add_field(name=f'{i}', value=f'{dic[i]}')
        await ctx.channel.send(embed=embed)


"""
This on_ready() function is a function that will be asynchronously when the programme starts.
Input:
        N/A
command:
        N/A
"""


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


"""
This delete_message() function, will delete 50 messages in he channel where the msg was sent.
Input:
        ctx -> The context (CONTEXT Object)
command:
    delete_message()
"""


@commands.command(description="A method that delete 50 messages in the channel where the message command was sent.",
                  brief="Deletes messages in a channel.")
async def delete_message(ctx):
    messages = await ctx.channel.history(limit=50).flatten()
    for message in messages:
        await message.delete()
        print("The content of message is:" + message.content)

    print("Work COMPLETED")
    await message_box("Congratulations", f"You just delete {len(messages)} message in this channel", ctx)


"""
This add_mienr() function, will add erc20 address to the list in channel where the msg was sent.
Input:
        ctx -> The context (CONTEXT Object)
command:
    add_miner 0x11111 
"""


@commands.command(description="A method that will add stats of a miner in eetermine.", brief="Adds miner")
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
        await message_box("Failed",
                          f"Hi {author_name},\n  The address you just entered is either wrong or already in the list.",
                          ctx)


# Show
"""
This show_miner() function, will show miner status and console.log the embed in the channel.
Input:
        ctx -> The context (CONTEXT Object)
command:
    delete_message()
"""


@commands.command(description="A method that will show miner stats in ethermine pool.", brief="show_miner_stats")
async def show_miner_stats(ctx):
    if len(addresses) < 0:
        await ctx.channel.send("HEY, You haven't add a miner yet!")
    else:
        await show_stats(ctx)


############################## Monitoring spam messages in the channel.
@commands.command(description="A method that will add arguments to word list and monitor messages.",
                  brief="add_miner arg1 arg2")
async def add_word(ctx, *args):
    if len(args) < 1:
        await ctx.channel.send("Hi, you need some arguments! Example: $add_word badword1 badword2 badword3")
    else:
        items = set(args)
        banned_item_list.update(items)
        await message_box("Succeeded",
                          "You have successfully added them to the list, duplicate items are not included.", ctx)


"""
This on_message() will monitor every message in the channel, if message contains one or more items in banned_item_list, user will be kicked out.
Input:
        ctx -> The context (CONTEXT Object)
command:
    delete_message()
"""


@bot.event
async def on_message(msg):
    # do some extra stuff here
    await bot.process_commands(msg)
    if msg.author == bot.user:
        return
    ctx = await bot.get_context(msg)
    member = msg.author
    content = msg.content
    print("The Content is " + str(content))
    word_in_banned_list = any(word in msg.content for word in banned_item_list)
    if word_in_banned_list and "$add_word" not in content:  # If msg itself is not a command and it's in the forbidden list
        await member.kick(reason='YOU Entered BAD WORD')
        await ctx.channel.send(f"{msg.author.mention} was kicked")
        await message_box("Reason", f"Forbidden Message Detected:\n {msg.content}", ctx)
        await msg.delete()


bot.add_command(add_word)
bot.add_command(add_miner)
bot.add_command(delete_message)
bot.add_command(show_miner_stats)
bot.run('TOKEN')

# DELETE_MESSAGE WORKS FINE
