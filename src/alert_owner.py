
#Sends an imail to a specified email address/ owners

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendMail():
    # me == my email address
    # you == recipient's email address
    me = "gianfrancocam123@gmail.com"
    you = "gfmacaraeg@gmail.com"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "UNKNOWN person detected!"
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).
    text = "The camera has shows an unknown person in your property"


    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)

    # Send the message via local SMTP server.
    s = smtplib.SMTP('localhost')
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(me, you, msg.as_string())
    s.quit()

# sendMail()