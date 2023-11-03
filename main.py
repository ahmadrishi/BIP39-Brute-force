from btc.bitcoin import BitCoin
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
from mnemonic import Mnemonic
import winsound
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second

def generate_string():
    mnemo = Mnemonic("english")
    #rangee = 24
    #choice = [secrets.choice(phrases) for _ in range(rangee)]
    #phrase = ' '.join(choice)
    memo = (mnemo.generate(strength=128)).split(' ')
    for i in range(random.randint(1, 12)):
        random.shuffle(memo)
    phrase = ' '.join(memo)
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

def process_btc():
    s = secrets.token_hex(32)
    e = secrets.token_hex(32)
    start_phrase = int(s, 16) + 1
    end_phrase = int(e, 16)
    for deci in range(start_phrase, end_phrase + 1, 1):
        hex = format(deci, 'X')
        pri, add = gen_key(hex)
        balance = get_balance(add)
        try:
            if balance > 0:
                run = False
                print("Private Key: ", pri)
                print("Address: ", add)
                print("Balance: ", balance)
        except:
            pass

def wallet_phrase():
    phrase = generate_string()
    num = random.randint(0, 11)
    name = phrase.split(' ')[num]
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
                with open('wallets.txt', 'a+') as f:
                    f.write(phrase + ':' + str(balance))
                    f.write('\n')
    except Exception as e:
        print(10 * '-')
    
    try:
            wallet_delete(name)
    except:
            return

def main():
    while True:
        wallet_phrase()

threads = []
num_threads = 50
for i in range(num_threads):
    thread = threading.Thread(target=main)
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

