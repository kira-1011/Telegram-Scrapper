import pickle
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
import os
import sys
import csv
import time

re = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"
SLEEP_TIME = 120

def clr():
    if os.name == 'nt':
        os.system('cls')

    else:
        os.system('clear')

def send_sms():

    f = open('vars.txt', 'rb')
    accs = []

    while True:

        try:
            accs.append(pickle.load(f))

        except EOFError:
            f.close()
            break

    print('Choose which account to be a sender: \n')

    i = 0

    for acc in accs:

        print(f'[{0}] {acc[2]}')
        i += 1

    ind = int(input(f'\nEnter choice: '))
    api_id = accs[ind][0]
    api_hash = accs[ind][1]
    phone = accs[ind][2]

    c = TelegramClient(f'sessions/{phone}', api_id, api_hash)
    c.connect()

    if not c.is_user_authorized():

        try:

            c.send_code_request(phone)
            code = input(f'Enter the login code for {phone}: ')
            c.sign_in(phone, code)

        except PhoneNumberBannedError:

            print(f'{phone} is banned!')
            print(f'Run manager.py to filter them')
            sys.exit()

    clr()

    members = "./members/members.csv"
    users = []

    with open(members, encoding='UTF-8') as f:

        rows = csv.reader(f, delimiter=",", lineterminator="\n")
        next(rows, None)

        for row in rows:
            user = {}
            user['username'] = row[0]
            user['id'] = int(row[1])
            user['access_hash'] = int(row[2])
            user['name'] = row[3]
            users.append(user)

    print(gr+"[1] send a direct message by user ID\n[2] send a direct message by username ")

    mode = int(input(gr+"Input : "+re))

    message = input(gr+"[+] Enter Your Message : "+re)

    for user in users:

        if mode == 2:

            if user['username'] == "":
                continue
            
            receiver = c.get_input_entity(user['username'])

        elif mode == 1:
            receiver = InputPeerUser(user['id'], user['access_hash'])

        else:
            print(re+"[!] Invalid Mode. Exiting.")
            c.disconnect()
            sys.exit()

        try:
            print(gr+"[+] Sending Message to:", user['name'])
            c.send_message(receiver, message.format(user['name']))

            print(gr+"[+] Waiting {} seconds".format(SLEEP_TIME))
            time.sleep(SLEEP_TIME)

        except PeerFloodError:

            print(
                re+"[!] Getting Flood Error from telegram. \n[!] Script is stopping now. \n[!] Please try again after some time.")
            
            c.disconnect()
            sys.exit()

        except Exception as e:
            print(re+"[!] Error:", e)
            print(re+"[!] Trying to continue...")
            continue

    c.disconnect()

    print("Done. Message sent to all users.")

send_sms()