#from btc.bitcoin import BitCoin
from bitcoinlib.wallets import Wallet, wallet_delete
import requests
import json
from blockcypher import get_wallet_balance
from time import sleep
from bit import Key
import hashlib
import random
import secrets
from config import eng_ph as phrases
import sys
import threading
import os
from mnemonic import Mnemonic
import winsound
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second

#counter_lock = threading.Lock()
#counter = 1

def generate_string():
    mnemo = Mnemonic("english")
    #rangee = 24
    #choice = [secrets.choice(phrases) for _ in range(rangee)]
    #phrase = ' '.join(choice)
    memo = mnemo.generate(strength=128)
    phrase = memo
    return phrase

def get_balance(address):
    res = requests.get(f'https://chainflyer.bitflyer.jp/v1/address/{address}').content
    try:
        balance = json.loads(res)['confirmed_balance']
    except Exception as e:
        print(res)
        return
    return balance

def gen_key(hex):
    privKey= Key.from_hex(hex)
    myAddress = privKey.address

    return privKey.to_wif(), myAddress

def wallet_phrase():
    phrase = generate_string()
    name = str(random.randint(1, 1515151651651651)) 
    try:
        try:
            w = Wallet.create(name, keys=phrase, network='bitcoin')
        except Exception as e:
            return
        
        for i in w.addresslist():
            balance = get_balance(i)
            if balance != 0:
                winsound.Beep(frequency, duration)
                print('Bingo!')
                with open('./wallets.txt', 'a+') as f:
                    f.write(phrase + ':' + str(balance))
                    f.write('\n')
    except Exception as e:
        print(10 * '-')
    
    try:
            wallet_delete(name)
    except:
            return

def worker():
    while True:
        wallet_phrase()

def main():
    counter = 1

    # Create and start 50 threads
    threads = [threading.Thread(target=worker) for _ in range(500)]
    for thread in threads:
        thread.start()

    try:
        while True:
            os.system("cls")
            print(counter)
            counter += 1
            #sleep(1)
    except KeyboardInterrupt:
        # Wait for all threads to finish before exiting
        for thread in threads:
            thread.join()

main()