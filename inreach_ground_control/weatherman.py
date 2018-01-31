from os import environ
import requests

from inreach_ground_control.forecast import Forecast

REPLY_URL = environ["INREACH_TEXT_MESSAGE_URL"]
API_KEY = environ["DARK_SKY_API_KEY"]

DEFAULT_DAYS = 3
DEFAULT_UNITS = 'auto'

class Weatherman():
    def __init__(self, message):
        query_params = message.query_params()
        self.forecast = Forecast(
            API_KEY,
            latitude=query_params['lat'],
            longitude=query_params['lon'],
            units=query_params['units'] or DEFAULT_UNITS
        )

        report = self.forecast.daily_report(
            days=query_params['days'] or DEFAULT_DAYS,
            start_offset_days=query_params['start_offset_days']
        )

        self.data = {
            "ReplyAddress": message.address,
            "ReplyMessage": report,
            "MessageId": message.text_msg_id,
            "Guid": message.text_msg_extid
        }

    def send_forecast(self):
        return requests.post(REPLY_URL, data=self.data)
