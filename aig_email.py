"""
American Iron Giant email helpers
"""
import smtplib
import typing
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from os.path import basename

import attr


@attr.s(auto_attribs=True)
class Email:
    """OO Helper around python's email support"""

    from_: str
    to: str
    subject: str
    message: str
    files: typing.List[str] = []

    def to_mime_multipart(self) -> MIMEMultipart:

        msg = MIMEMultipart()
        msg["From"] = self.from_
        msg["To"] = self.to
        msg["Subject"] = self.subject
        msg["Date"] = formatdate(localtime=True)
        message = self.message
        msg.attach(MIMEText(message))

        # attachments
        for file in self.files:
            with open(file, "rb") as fil:
                part = MIMEApplication(fil.read(), Name=basename(file))
            # After the file is closed
            part["Content-Disposition"] = 'attachment; filename="%s"' % basename(file)
            msg.attach(part)

        return msg


@attr.s(auto_attribs=True)
class SMTPServer:
    """
    Wrapper around the smtplib server to simplify sending mail.
    """

    username: str
    password: str
    hostname: str
    port: int

    # TODO: be nice to make this async
    def send(self, email: Email) -> None:
        """
        Send email_message using this server.

        :param email: Holds the content, files attachments, to and from lines, subject, etc.
        """

        mail_server = smtplib.SMTP(self.hostname, self.port)
        mail_server.starttls()
        mail_server.login(self.username, self.password)
        mail_server.sendmail(
            email.from_,
            email.to,
            email.to_mime_multipart().as_string(),
        )
        mail_server.quit()
