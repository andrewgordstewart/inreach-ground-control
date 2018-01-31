import email
import re
import requests
from urllib import parse as urllib_parse

from bs4 import BeautifulSoup
import imapclient
from message import Message

class Digester():
    """
    Digest emails sent to <username> on the <host> IMAP server.
    Unread emails _that were sent by an inreach device_ are locally persisted using the db_session.

    Attributes
    ----------

    db_session: sqlalchemy.orm.sessionmaker(bind=<sqlalchemy.engine.base.Engine>)
        A database session which contains a 'messages' table (See the message module.)
    imap_obj: imapclient.IMAPClient
        IMAP client connecting to the <username>'s email on the <host> IMAP server. The 'INBOX'
        folder is selected.

    """

    def __init__(self, db_session, host, username, password=None, ssl=True, port=993):
        self.db_session = db_session
        password = password or input("Please enter your password.")

        self.imap_obj = imapclient.IMAPClient(host, ssl=ssl, port=port)
        self.imap_obj.login(username, password)
        self.imap_obj.select_folder('INBOX')

    def check_emails(self, search='UNSEEN'):
        """
        Checks for emails in the INBOX matching search term.
        If a matching email was sent from an Inreach device, persists relevant information
        using the provided db_session

        :return: True
        """
        email_ids = self.imap_obj.search(search)
        emails = self.imap_obj.fetch(email_ids, "RFC822")

        parsed_emails = []

        for email_id, each_email in emails.items():
            message = email.message_from_bytes(each_email[b"RFC822"])

            try:
                self.validate(message)
            except(InvalidEmailError) as e:
                print("Email is invalid: {}".format(e.message))
            else:
                """
                GMail responds with multi-part messages. We're using BeautifulSoup to parse
                the message, so we select the text/html version.
                """

                address = message.get('To')
                html_message = next(m for m in message.get_payload() if m.get_content_type() == 'text/html')
                body = html_message.get_payload(decode=True)

                try:
                    self.parse_and_persist(body, address)
                except:
                    self.imap_obj.set_flags([email_id], 'UNSEEN')

        return True

    @staticmethod
    def validate(message):
        """
        Validates that the message was actually sent from an Inreach device.

        :message: email.message.Message
            Message to be validated.
        :return: True
        """
        auth_results = dict(message.items())["ARC-Authentication-Results"]
        if not 'dkim=pass header.i=@garmin.com' in auth_results:
            raise NotFromGarminError("The email did not come from Garmin: {}".format(auth_results))

        pass

    def parse_and_persist(self, body, address):
        """
        Parses and persists an email's body from an inreach text message as a Message.

        Currently, inreach emails all share the following properties:
        subject: inReach message from Andrew Stewart
        mailed-by: 	inreacheml.garmin.com
        signed-by: garmin.com
        body: <message>

            View the location or send a reply to <name>: <url>

            <name> sent this message from: Lat <lat> Lon <lon>\n\n<some other stuff>

        :param body: str
           The email body from an inreach 'text message'.

        :param address: str
           The recipient email address of the inreach message.
        """

        soup = BeautifulSoup(body, 'html.parser')

        paragraphs = soup.find_all('p')

        # "This message was sent to you using ..."
        paragraphs.pop() # (discard)

        # "Do not reply directly to this message."
        paragraphs.pop() # (discard)

        # <user> sent this message from: Lat [lat] Lon [lon]
        coords_p = paragraphs.pop()
        # If the GPS signal is small, the coordinates may be 0, 0.
        # Otherwise, they would almost surely have some decimal precision.
        pattern = re.compile(r'-?\d+\.?\d*')
        latitude, longitude = pattern.findall(str(coords_p))

        # View the location or send a reply to [user]: <a 'href'=[url]><url></a>
        reply_url_p = paragraphs.pop()
        reply_url = reply_url_p.find('a').attrs['href']

        query_string = urllib_parse.urlparse(reply_url).query
        text_msg_extid = urllib_parse.parse_qs(query_string)['extId'][0]

        reply_html = requests.get(reply_url).content
        reply_soup = BeautifulSoup(reply_html, 'html.parser')

        text_msg_id = int(reply_soup.find('input', attrs={'id': 'MessageId'}).attrs['value'])

        # The remainder of the paragraph tags are from the message.
        # Note that preset messages don't allow newlines, meaning there should only be one
        # remaining paragraph tag.
        text_msg = '\n'.join([str(p.get_text(strip=True)) for p in paragraphs])

        message = Message(
            address=address,
            text_msg_extid=text_msg_extid,
            text_msg_id=text_msg_id,
            text_msg=text_msg,
            latitude=latitude,
            longitude=longitude,
            response_sent=False
        )

        # Because SQLAlchemy Core doesn't support upsert...
        # TODO: Switch to using SQLAlchemy Core and use UPSERT to deal with the unique constraint on
        #       text_msg_extid
        self.db_session.add(message)

        try:
            self.db_session.commit()
        except:
            # TODO: Only except the correct error. (psycopg2.IntegrityError?)
            # TODO: Log something here.
            self.db_session.rollback()
            pass

class NotFromGarminError(Exception):
    """
    Indicates that an email is believed not to be sent from an Inreach device.
    """
    pass

if __name__ == "__main__":
    """
    Since I can't be bothered to mock an IMAP server to run tests, here's some live "testing".
    """

    from database import db_session
    session = db_session()

    d = Digester(session, 'imap.gmail.com', 'inreach.ground.control', password='%MsUZV6RT3PvQGZXUx8')
    d.check_emails(search='UNSEEN')
