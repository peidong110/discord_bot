import requests
import discord
from discord.ext import commands
from datetime import datetime
import re

bot = commands.Bot(command_prefix='#')
miners = []
endpoint = 'https://api.ethermine.org'
reduce_digit_list = ['reportedHashrate', 'currentHashrate', 'averageHashrate']
regular_items = ['validShares', 'staleShares', 'activeWorkers']

async def get_data(miner_address):
    results = {}
    request_url = endpoint + '/miner/' + miner_address + '/currentStats'
    res = requests.get(request_url)
    if res.status_code == 200:
        print(res.json())
        res = res.json()
        keys = res['data'].keys()
        for item in keys:
            if item in reduce_digit_list:
                values = str(res['data'][item])[0:3]
                updatedItem = item[0].upper() + item[1:].replace("Hashrate", " Hashrate")
                results[updatedItem] = values
            elif item in regular_items:
                values = str(res['data'][item])
                updatedItem = item[0].upper() + item[1:].replace("Share", " Share").replace("Workers", " Workers")
                results[updatedItem] = values
            elif item == 'unpaid':
                unpaid_balance = '0.' + str(res['data'][item])[0:5]
                results['Unpaid ETH'] = unpaid_balance
            elif item == 'usdPerMin':
                value = res['data']['usdPerMin']
                print("usd per min = :" + str(value))
                value *= 60 * 24
                # print(format(321, ".2f"))
                results['USD Per Day'] = round(value, 2)
            #return rate
            results['Rate:'] = round(1-res['data']['staleShares']/(res['data']['staleShares']+res['data']['validShares']),4)
            # else:
            #     results[item] = str(res['data'][item])
        print("RESULT:")
        print(results)
    else:
        print("Potential Error")
    return results


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


def is_valid_address(address):
    if len(address) == 42 and address[0:2] == "0x" and address[2:].isalnum():
        return True
    else:
        return False


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('$show miner'):
        content = message.content.split(" ")
        if is_valid_address(content[2]):
            dic = await get_data(content[2])
            embed = discord.Embed(title="Miner Stats: ", color=0xeee657)
            # give info about you here

            for item in dic:
                embed.add_field(name=f'{item}', value=f'{dic[item]}')
            # Shows the number of servers the bot is member of.
            # give users a link to invite thsi bot to their server
            # embed.add_field(name="Invite", value="[Invite link](<insert your OAuth invitation link here>)")

            await message.channel.send(embed=embed)
        else:
            await message.channel.send('Sorry, ' + message.content + " you just entered is not a valid erc20 address.")

        print("Content:" + str(content))
        # await message.channel.send('Hello World!' + message.content)

    # print("hello"+str(message))



bot.run('TOKEN')
