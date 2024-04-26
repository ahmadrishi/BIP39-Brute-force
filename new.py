# from web3 import Web3
import secrets
import requests
import json
from mnemonic import Mnemonic
# from btc.bitcoin import BitCoin
from bitcoinlib.wallets import Wallet, wallet_delete

# bitcoin = BitCoin(BitCoin.HttpProvider(endpoint_uri='https://morning-special-meme.btc.discover.quiknode.pro/f1169d5a23f874230f4e4e80ffcf664ceb0b118e/', rpcuser='', rpcpassword=''))
# w3 = Web3(Web3.HTTPProvider('https://long-weathered-diamond.discover.quiknode.pro/ec5803112411ec3bd8e6641bac1427ecfdd13da8/'))
mn = Mnemonic(language='english')
def generate_string():
    # rangee = 12
    # choice = secrets.token_bytes(rangee)
    # phrase = str(choice)
    phrase = mn.generate(strength=128)
    return phrase

# w3.eth.account.enable_unaudited_hdwallet_features()
run = True
# if w3.is_connected() is False:
#     quit()

while run:
    phrase = generate_string()
    
    try:
        try:
            wallet_delete('nice')
        except:
            pass
        w = Wallet.create('nice', keys=phrase, network='bitcoin')
        for i in w.addresslist():
            balance_url = f'https://mempool.space/api/address/{i}/txs/chain'
            res = requests.get(balance_url).content
            data = len(json.loads(res))
            print(data)
            if data > 0:
                print(phrase)
    except Exception as e:
        print(str(e))
        pass
    
    # balance = 0
    # balance_btc = 0
    # try:
    #     acc = w3.eth.account.from_mnemonic(phrase)
    #     balance = w3.eth.get_balance(acc.address)
    #     print(acc.address)
    #     bsc.write(str(balance) + ':' + acc.address + ':' + phrase)
    #     bsc.write('\n')
    #     noWallet = noWallet + 1
    #     if noWallet % 100 == 0:
    #         print("Number of Wallets: " + str(noWallet))
    # except Exception as e:
    #     #print(e)
    #     pass

    # if balance > 0:
    #     winsound.Beep(frequency, duration)
    #     print(phrase)
    #     log.write(phrase)
    #     log.write('\n')
    #     run = False
    
