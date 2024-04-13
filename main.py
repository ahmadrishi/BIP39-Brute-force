#from btc.bitcoin import BitCoin
from bitcoinlib.wallets import Wallet, wallet_delete
import requests
import json
from blockcypher import get_wallet_balance
import random
import secrets
from mnemonic import Mnemonic
import threading

def generate_string():
    mnemo = Mnemonic("english")
    phrase = mnemo.generate(strength=128)
    return phrase

def get_balance(address):
    res = requests.get(f'https://chainflyer.bitflyer.jp/v1/address/{address}').content
    try:
        balance = json.loads(res)['confirmed_balance']
    except Exception as e:
        print(res)
        return
    return balance

def wallet_phrase():
    phrase = generate_string()
    name = str(random.randint(1, 1515151651651651)) 
    try:
        w = Wallet.create(name, keys=phrase, network='bitcoin')
        for addr in w.addresslist():
            balance = get_balance(addr)
            if balance != 0:
                print(f'{addr}:{phrase}:{balance}')
                with open('./wallets.txt', 'a+') as f:
                    f.write(f'{addr}:{phrase}:{balance}\n')
        wallet_delete(name)
    except Exception as e:
        print("Error processing wallet")

def worker():
    while True:
        wallet_phrase()

def main():
    threads = [threading.Thread(target=worker) for _ in range(500)]
    for thread in threads:
        thread.start()

    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        print("Interrupted by user")

main()
