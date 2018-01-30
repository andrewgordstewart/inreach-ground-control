from collections import defaultdict
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates
from sqlalchemy import Column, Integer, String, Float, Boolean

Base = declarative_base()

BOOLEAN_QUERY_KEYS = ["daily", "hourly"]
STRING_QUERY_KEYS = ["units"]
NUMERIC_QUERY_KEYS = ["lat", "lon"]
QUERY_KEYS = BOOLEAN_QUERY_KEYS + STRING_QUERY_KEYS + NUMERIC_QUERY_KEYS
TRUTHY_QUERY_VALUES = ["yes", "y", "true", "t"]
FALSY_QUERY_VALUES = ["no", "n", "false", "f"]

class Message(Base):
    """
    A stored inreach message.

    Fields
    ------
    :param id: int
        Primary key

    :param address: str
        The email address owning the message.

    :param text_msg_extid: str
        A GUID identifying the received inreach message.

    :param text_msg_id: int
        An integer id identifying the received inreach message.

    :param text_msg: str
        The message written by the inreach user.

    :param latitude: int
        The latitudinal coordinate of the inreach user at the time the message was sent.

    :param longitude: int
        The longitudinal coordinate of the inreach user at the time the message was sent.

    :param response_sent: bool
        Indicates whether the inreach user has been sent a response containing the weather report.
    """
    __tablename__ = 'messages'

    id = Column(Integer,            primary_key=True)
    address = Column(String,        nullable=False)
    text_msg_extid = Column(String, nullable=False, unique=True)
    text_msg_id = Column(Integer,   nullable=False)
    text_msg = Column(String,       nullable=False)
    latitude = Column(Float,        nullable=False)
    longitude = Column(Float,       nullable=False)
    response_sent = Column(Boolean, nullable=False)

    def __repr__(self):
        """
        Overwrites default magic __repr__ method.
        """
        return f"<Message(address='{self.address}', text_msg_extid='{self.text_msg_extid}', text_msg_id='{self.text_msg_id}', text_msg='{self.text_msg}', latitude='{self.latitude}', longitude={self.longitude}', response_sent='{self.response_sent}')>"

    def query_params(self):
        """
        Parses options contained in the text_msg field (sent from inreach device)

        text_msg is expected to be of the following form

        '''
        wx <start_time>
        <opt1>=<val1>
        <opt2>=<val2>
        <etc>
        '''

        This method is case insensitive -- text_msg is downcased before being parsed.

        :return: :class: Query parameters <collections.DefaultDict> object
        :rtype: collections.DefaultDict
        """
        opts = defaultdict(lambda : None)

        lines = self.text_msg.lower().replace('wx ', '').splitlines()

        start_time = lines[0]
        if start_time == "now":
            start_offset_days = 0
        else:
            start_offset_days = int(start_time.replace(' days', ''))
        opts["start_offset_days"] = start_offset_days

        for line in lines[1:]:
            key, value = line.split('=')

            if key not in QUERY_KEYS:
                continue

            if key in BOOLEAN_QUERY_KEYS:
                opts[key] = (value in TRUTHY_QUERY_VALUES)
            elif key in NUMERIC_QUERY_KEYS:
                opts[key] = float(value)
            else:
                opts[key] = value

        # "latitude" and "longitude" are required parameters to a weather forecast.
        # The default values should be supplied by the inreach user's current position.
        # Of course, defaults are _only_ overwritten when both coordinates are supplied

        coordinates_specified = (opts["lat"] and opts["lon"])

        opts["lat"] = opts["lat"] if coordinates_specified else self.latitude
        opts["lon"] = opts["lon"] if coordinates_specified else self.longitude

        return opts

    @validates('text_msg')
    def validate_text_msg(self, key, text_msg):
        assert text_msg[0:3] == 'wx '
        return text_msg
