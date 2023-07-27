from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, PhoneNumberBannedError
import sys
import csv
import time

api_id = int(input(f'\nEnter API ID: '))
api_hash = str(input(f'Enter API Hash: '))
phone = str(input(f'Enter Phone Number: '))

sent = 0
not_sent = 0
SLEEP_TIME = 60
c = TelegramClient(f'sessions/{phone}', api_id, api_hash)
c.connect()

if not c.is_user_authorized():

    try:

        c.send_code_request(phone)
        code = input(f'Enter the login code for {phone}: ')
        c.sign_in(phone, code)

    except PhoneNumberBannedError:

        print(f'{phone} is banned!')
        sys.exit()

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

print("[1] send a direct message by user ID\n[2] send a direct message by username ")

mode = int(input("Input : "))

message = input("[+] Enter Your Message : ")

for user in users:

    if mode == 2:

        if user['username'] == "":
            continue
        
        receiver = c.get_input_entity(user['username'])

    elif mode == 1:
        receiver = InputPeerUser(user['id'], user['access_hash'])

    else:
        print("[!] Invalid Mode. Exiting.")
        c.disconnect()
        sys.exit()

    try:
        print("\n[+] Sending Message to:", user['name'])
        c.send_message(receiver, message.format(user['name']))

        print("[+] Waiting {} seconds".format(SLEEP_TIME))
        time.sleep(SLEEP_TIME)
        sent += 1
        print("success")

    except PeerFloodError:

        print(
            "[!] Getting Flood Error from telegram. \n[!] Script is stopping now. \n[!] Please try again after some time.")
        not_sent += 1
        
        c.disconnect()
        # sys.exit()

    except Exception as e:
        not_sent += 1
        print("[!] Error:", e)
        print("[!] Trying to continue...")
        continue

c.disconnect()

print(f"Done. Message sent to {sent} users of {len(users)}")