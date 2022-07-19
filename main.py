""""
The American Iron Front Discord Server's Iron Giant bot.

Currently scrapes a single channel for protest images and forwards them on via email for further analysis.
"""
import asyncio
import datetime
import logging
import os

import discord
from dotenv import load_dotenv

from aig_email import Email, SMTPServer
from aig_os import move_files, tar_up
from web import get_urls, is_image, download_image

load_dotenv()
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("DISCORD_TOKEN")
TARGET_CHANNEL = os.getenv("CHANNEL")
DOWNLOAD_DIRECTORY = os.getenv("DOWNLOAD_DIRECTORY")

client = discord.Client()


async def flush_image_directory() -> None:
    """
    A task loop that:
    1) Wakes up at 1am every day
    2) Tars everything in the downloads directory
    3) Emails that file out
    4) Removes everything in the downloads directory
    """
    await client.wait_until_ready()

    # guild = discord.utils.get(client.guilds, name=GUILD)
    # general_channel = discord.utils.get(guild.channels, name="general")

    while True:

        # get tomorrow at 1am
        target_time = datetime.datetime.combine(
            datetime.datetime.today(), datetime.time.min
        ) + datetime.timedelta(days=1, hours=1)

        logging.info(f"Targeting {target_time}")

        seconds_until = target_time - datetime.datetime.now()

        await asyncio.sleep(seconds_until.seconds)

        # If no images, wait until the next day
        if not os.listdir(DOWNLOAD_DIRECTORY):
            continue

        filename = tar_up(DOWNLOAD_DIRECTORY, "images")

        email = Email(
            from_=os.getenv("FROM_EMAIL"),
            to=os.getenv("TO_EMAIL"),
            subject=f"Images from {TARGET_CHANNEL} for {datetime.datetime.today()}",
            message="See attached files",
            files=[filename],
        )

        server = SMTPServer(
            username=os.getenv("SMTP_USERNAME"),
            password=os.getenv("SMTP_PASSWORD"),
            hostname=os.getenv("SMTP_HOST"),
            port=int(os.getenv("SMTP_PORT")),
        )

        server.send(email)

        move_files(DOWNLOAD_DIRECTORY, os.getenv("ARCHIVE_DIRECTORY"))

        logging.info("Successfully emailed and ")


client.loop.create_task(flush_image_directory())


@client.event
async def on_ready():
    """Primarily a debugging callback to ensure we've connected to discord correctly"""
    logging.info(f"{client.user} has connected to Discord!")

    guild = discord.utils.get(client.guilds, name=os.getenv("DISCORD_GUILD"))

    logging.info(
        f"{client.user} is connected to the following guild:\n {guild.name}(id: {guild.id})"
    )


@client.event
async def on_message(message):
    """
    Called by discord.py when a new message is sent in any channel

    We'll extract image urls to download, and mark any message with images with 👀

    :param message: The discord message
    """

    # prevent us from ever responding to our own messages
    if message.author == client.user:
        return

    # See if the messages from protest photos
    if not message.channel.name == TARGET_CHANNEL:
        return

    image_urls = [url for url in get_urls(message) if is_image(url)]

    if image_urls:
        await message.add_reaction("👀")
        for image_url in image_urls:
            download_image(image_url, DOWNLOAD_DIRECTORY)


logging.info("Running")

client.run(TOKEN)
