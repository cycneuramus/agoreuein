import asyncio
import logging
import os
from random import randint

import names
import requests
from telethon import TelegramClient, errors
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.types import InputPhoneContact

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.INFO
)

api_id = os.environ["API_ID"]
api_hash = os.environ["API_HASH"]
my_phone_number = os.environ["MY_PHONE_NUMBER"]
msg = os.environ["MSG"]

client = TelegramClient(my_phone_number, api_id, api_hash)


async def get_random_recipient():
    phone_number_raw = requests.get("https://api.1920.in").json()
    return f"+{phone_number_raw}"


async def add_contact(recipient_phone):
    contact = InputPhoneContact(
        client_id=0,
        phone=recipient_phone,
        first_name=names.get_first_name(),
        last_name=names.get_last_name(),
    )

    # not every phone number is associated with a Telegram account
    try:
        new_contact = await client(ImportContactsRequest([contact]))
        if "user_id" not in new_contact.stringify():
            logging.error(f"Failed to add contact {recipient_phone}.")
        else:
            return new_contact

    except errors.FloodWaitError as e:
        logging.info(f"Flood limit hit, sleeping {e.seconds} seconds.")
        await asyncio.sleep(e.seconds)


async def send_msg(new_contact):
    msg_result = await client.send_message(new_contact.users[0], msg)
    logging.info(msg_result)


async def main():
    async with client:
        while True:
            await client.connect()

            if not await client.is_user_authorized():
                await client.send_code_request(my_phone_number)
                await client.sign_in(my_phone_number, input("Enter the code: "))

            recipient_phone = await get_random_recipient()
            new_contact = await add_contact(recipient_phone)

            if new_contact is not None:
                await send_msg(new_contact)

            seconds = randint(600, 1800)
            logging.info(f"Sleeping for {seconds} seconds")

            await asyncio.sleep(seconds)


client.loop.run_until_complete(main())
