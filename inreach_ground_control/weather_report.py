import json
from os import environ

import click

from inreach_ground_control.database import db_session
from inreach_ground_control.forecast import Forecast
from inreach_ground_control.message import Message
from inreach_ground_control.weatherman import Weatherman

@click.command()
def cli():
    messages = db_session.query(Message).filter(Message.response_sent == False).all()

    for message in messages:
        query_params = message.query_params()

        response = Weatherman(message).send_forecast()

        if response.status_code == 200 and json.loads(response.text)['Success'] is True:
            # NB: json.loads may throw an error when the POST request was unsuccessful,
            # since inreach.garmin.com returns an html "Error page", along with status code 200.
            message.response_sent = True
            db_session.commit()

    db_session.remove()
