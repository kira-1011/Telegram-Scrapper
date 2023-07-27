from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
import csv
import sys
from telethon.tl.types import UserStatusOffline
from time import sleep
from telethon.tl.functions.channels import GetFullChannelRequest

def write(target_group,user):

    user_status = ""
    name = ""
    
    if user.username:
        username= user.username
    else:
        username= ""

    if user.first_name:
        first_name= user.first_name
    else:
        first_name= ""
    
    if user.last_name:
        last_name= user.last_name
    else:
        last_name= ""

    if isinstance(user.status,UserStatusOffline):
        user_status = user.status.was_online
    else:
        user_status = type(member.status).__name__

    name = (first_name + ' ' + last_name).strip()

    writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id, user_status])

api_id = int(input('\nEnter API ID: '))
api_hash = str(input('Enter API Hash: '))
phone = str(input('Enter Phone Number: '))

group_name = input("Enter the name of the group without the @: ")

c = TelegramClient(f'sessions/{phone}', api_id, api_hash)
c.start()
c.connect()

if not c.is_user_authorized():

    try:
        c.send_code_request(phone)
        code = input(f' Enter the login code for {phone}: ')
        c.sign_in(phone, code)

    except PhoneNumberBannedError:
        print(f'{phone} is banned!')
        sys.exit()

group = c.get_entity(group_name)
target_grp = "t.me/" + group_name

members = []
members = c.iter_participants(group, aggressive=True)

channel_full_info = c(GetFullChannelRequest(group))
cont = channel_full_info.full_chat.participants_count  

with open("members\\members.csv", "w", encoding='UTF-8') as f:
    
    writer = csv.writer(f, delimiter=",", lineterminator="\n")
    writer.writerow(['username', 'user id', 'access hash', 'group', 'group id','status'])

    try:

        for index,member in enumerate(members):

            print(f"{index+1}/{cont}", end="\r")
            
            if index % 100 == 0:
                sleep(3)
            
            if not member.bot:
                write(group,member)     

    except:
        print("\nThere was a FloodWaitError, but check members.csv.")
    
print(f"\nUsers saved in the csv file")