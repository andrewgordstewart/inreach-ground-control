from os import environ

import click

from inreach_ground_control.database import db_session
from inreach_ground_control.forecast import Forecast
from inreach_ground_control.message import Message
from inreach_ground_control.weatherman import Weatherman

@click.command()
@click.option('--guid', help='guid of the inReach text message')
def cli(guid):
    click.echo(f"Sending forecast for message {guid} to Andrew!")

    message = db_session.query(Message).filter(Message.text_msg_extid == guid).first()
    query_params = message.query_params()

    click.echo(f"Would send POST request with data {query_params}")
    Weatherman(message).send_forecast()
