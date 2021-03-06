#!/usr/bin/env python3

import asyncio
import logging
import os
from random import randint

import names
from phone_gen import PhoneNumber
from telethon import TelegramClient, errors
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.types import InputPhoneContact

logging.basicConfig(
    format="%(asctime)s %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)


async def sleep_through_flood(error):
    seconds = error.seconds
    minutes = round(seconds / 60)
    logging.info(f"Flood limit hit, sleeping for {minutes} minutes.")
    await asyncio.sleep(seconds)


async def get_random_recipient():
    p = PhoneNumber("RU")
    return p.get_mobile()


async def add_contact(client, recipient_phone):
    random_firstname = names.get_first_name()
    random_lastname = names.get_last_name()

    contact = InputPhoneContact(
        client_id=0,
        phone=recipient_phone,
        first_name=random_firstname,
        last_name=random_lastname,
    )

    try:
        new_contact = await client(ImportContactsRequest([contact]))
        logging.info(
            f'Adding {recipient_phone} ("{random_firstname} {random_lastname}")'
        )

        if "user_id" not in new_contact.stringify():
            logging.error(f"Failed to add contact {recipient_phone}")
            logging.debug(new_contact.stringify())
        else:
            return new_contact
    except errors.FloodWaitError as error:
        sleep_through_flood(error)


async def send_msg(client, recipient):
    msg = os.environ["MSG"]
    logging.info("Sending message")

    msg_result = await client.send_message(recipient, msg)
    logging.info(msg_result)


async def main():
    api_id = os.environ["API_ID"]
    api_hash = os.environ["API_HASH"]
    my_phone_number = os.environ["MY_PHONE_NUMBER"]

    client = TelegramClient(my_phone_number, api_id, api_hash)

    async with client:
        while True:
            if not client.is_connected():
                await client.connect()

                if not await client.is_user_authorized():
                    await client.send_code_request(my_phone_number)
                    await client.sign_in(my_phone_number, input("Enter the code: "))

            logging.info("Checking for account restriction")
            try:
                me = await client.get_me()
                logging.debug(me)

                if me.restricted:
                    hours = 48
                    logging.error(f"Account restricted, sleeping {hours} hours")
                    await asyncio.sleep(hours * 60 * 60)
            except errors.FloodWaitError as error:
                sleep_through_flood(error)

            recipient_phone = await get_random_recipient()
            new_contact = await add_contact(client, recipient_phone)

            if new_contact is not None:
                await send_msg(client, new_contact.users[0])

            seconds = randint(60, 300)
            minutes = round(seconds / 60)
            logging.info(f"Sleeping for {minutes} minutes")
            await asyncio.sleep(seconds)


if __name__ == "__main__":
    asyncio.run(main())
