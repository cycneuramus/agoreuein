# Agoreuein

> "The first casualty, when war comes, is truth."

This is a Python script that periodically tries to send a message, pre-defined by you, to a random Russian phone number over Telegram. I wrote this as a proof-of-concept for trying to break the barrier of Russian state propaganda concerning the invasion of Ukraine. The inspiration – as well as the phone number API – comes from https://1920.in, developed by [squad303](https://github.com/squad303/squad303app).

Note that not all selected phone numbers will be associated with a Telegram account. As such, error messages are to be expected.

## WARNING

This program is not a bot, but uses the Telegram API to sends its messages directly from an account that you control. In order for this to work, the program must first add the intended recipient to your contacts. **Contacting people you don't know en-masse is considered to be spam.** It is highly likely that your account will be reported as such and limited for a time. Repeated offences may impose further limits and, ultimately, block your account altogether. For more information, see Telegram's [Spam FAQ](https://telegram.org/faq_spam).

## Note on messages

The point of this program is not to harass people, but to engage in civil discourse with those who may be victims of state-sponsored disinformation and propaganda. As such, I would encourage you to refrain from sending inflammatory or unnecessarily polarizing messages.

## Usage

### Docker

Clone this repo: 
```
git clone https://github.com/cycneuramus/agoreuein
```

Create and populate the `.env` file (see `.env_example` for details):
```
cd agoreuein
vim .env
```

Build the container and authorize your Telegram account on first run:
```
docker-compose build
docker-compose run agoreuein
```

Now, either keep the container running, or cancel the foreground process and start it in the background:
```
docker-compose up -d
```

### Bare metal
Yes, I've made this tiny script run in Docker. There is technically no need for this, of course, but it's what I do to keep my environment clean and reproducible, and I provide this repo as-is. If you prefer bare metal, you would need to:

+ `pip install names requests telethon`
+ `export API_ID=<your Telegram API id>` 
+ `export API_HASH=<your Telegram API hash>`
+ `export MY_PHONE_NUMBER=<your Telegram phone number>`
+ `export MSG=<the message to be send>`

Alternatively, instead of setting environment variables, you may edit `agoreuein.py` directly to add the appropriate values. 
