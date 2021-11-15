import requests
import discord
miners = []
endpoint = 'https://api.ethermine.org'
reduce_digit_list = ['reportedHashrate', 'currentHashrate', 'averageHashrate']
regular_items = ['validShares', 'staleShares', 'activeWorkers']


def is_valid_address(address):
    if len(address) == 42 and address[0:2] == "0x" and address[2:].isalnum():
        return True
    else:
        return False
    
def get_data(miner_address):
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
