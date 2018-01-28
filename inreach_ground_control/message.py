from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer,            primary_key=True)
    text_msg_extid = Column(String, nullable=False, unique=True)
    text_msg = Column(String,       nullable=False)
    latitude = Column(Float,        nullable=False)
    longtitude = Column(Float,      nullable=False)
    response_sent = Column(Boolean, nullable=False)

    def __repr__(self):
        """
        Overwrites default magic __repr__ method.
        """
        return f"<Message(text_msg_extid='{self.text_msg_extid}', text_msg='{self.text_msg}', latitude='{self.latitude}', longitude={self.longitude}', response_sent='{self.response_sent}')>"
