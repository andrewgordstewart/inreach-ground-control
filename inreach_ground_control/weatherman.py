from inreach_ground_control.forecast import Forecast
from os import environ
import requests

###
# For the moment, these will be stored as environment variables.
# They should instead be read from the email sent to REPLY_ADDRESS
# TODO: Fix this
MESSAGE_ID    = environ["MESSAGE_ID"]
###

REPLY_URL     = "https://inreach.garmin.com/TextMessage/TxtMsg"

class Weatherman():
    def __init__(self, forecast, message):
        weather_report = ''.join(forecast.daily_report().split())
        self.data = {
            "ReplyAddress": message.address,
            "ReplyMessage": weather_report,
            "MessageId": MESSAGE_ID,
            "Guid": message.text_msg_extid
        }

    def send_forecast(self):
        return requests.post(REPLY_URL, data=self.data)
