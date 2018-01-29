from inreach_ground_control.forecast import Forecast
from os import environ
import requests

###
# For the moment, these will be stored as environment variables.
# They should instead be read from the email sent to REPLY_ADDRESS
# TODO: Fix this
REPLY_ADDRESS = environ["REPLY_ADDRESS"]
MESSAGE_ID    = environ["MESSAGE_ID"]
GUID          = environ["MESSAGE_GUID"]
###

API_KEY       = environ["DARK_SKY_API_KEY"]
REPLY_URL     = "https://inreach.garmin.com/TextMessage/TxtMsg"

class Weatherman():
    def __init__(self, forecast):
        self.forecast = forecast
        self.data = {
            "ReplyAddress": REPLY_ADDRESS,
            "ReplyMessage": ''.join(fio.daily_report().split()),
            "MessageId": MESSAGE_ID,
            "Guid": GUID
        }

    def send_forecast(self):
        return requests.post(REPLY_URL, data=self.data)
