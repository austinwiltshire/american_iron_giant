"""
American Iron Giant url and web stuff
"""
import logging
import os
from urllib import parse

import attr
import requests
import validators
import posixpath

from discord.message import Message


@attr.s(auto_attribs=True)
class Url:
    """Gives an OO-lite interface for a url"""

    full_url: str

    @property
    def path(self) -> str:
        """
        From www.example.com/path/to/file.gz we extract /path/to/file.gz

        :return: The path
        """
        return parse.urlparse(self.full_url).path

    @property
    def file_name(self):
        """
        From www.example.com/path/to/file.gz we extract file.gz

        :return: The filename
        """
        return posixpath.split(self.path)[-1]

    @property
    def file_type(self) -> str:
        """
        From www.example.com/path/to/file.gz we extract gz

        :return: The file type
        """
        return posixpath.splitext(self.file_name)[-1]

    def get(self) -> requests.Response:
        """
        Does a HTTP GET on the full url using the requests library

        :return: The result of requests.get on the full url
        """
        return requests.get(self.full_url)


def get_urls_in_attachments(message: Message) -> [Url]:
    """
    Looks at a discord.py message object and extracts any urls that are added as attachments

    :param message: The discord.py message
    :return: A list (possibly empty) of Urls found as attachments
    """
    return [Url(attachments.url) for attachments in message.attachments]


def get_urls_in_message(message: Message) -> [Url]:
    """
    Get urls in the actual content of a message

    :param message: The discord.py message
    :return: A list (possibly empty) of Urls found in the content of a message
    """
    return [Url(token) for token in message.content.split(" ") if validators.url(token)]


def get_urls(message: Message) -> [Url]:
    """
    Gets urls in a discord.py message--both in attachments and content

    :param message: The discord.py message
    :return: A list (possibly empty) of Urls found in a discord.py message
    """
    return get_urls_in_attachments(message) + get_urls_in_message(message)


def is_image(potential_image_url: Url) -> bool:
    """
    Predicate that determines whether a url points to an image file or not. We only look for jpg or png at this time.

    :param potential_image_url: The url to check
    :return: True if it's a jpg or png, false otherwise
    """
    return potential_image_url.file_type in [".jpg", ".png"]


def download_image(img_url: Url, download_directory: str) -> None:
    """
    Download an image at img_url to the download_directory

    :param img_url: A url, assumed to be an image, to download
    :param download_directory: The directory (relative to .) to download to. If it doesn't exist, we'll create it.
    """
    # TODO: pull out this file getting logic into some common lib that both this and the reddit scraper can use
    if not os.path.exists(download_directory):
        os.mkdir(download_directory)

    request = img_url.get()
    with open(
        os.path.join(download_directory, img_url.file_name),
        "wb",
    ) as outfile:
        outfile.write(request.content)
    logging.info(f"Saved image to {download_directory} directory: {img_url.file_name}")
