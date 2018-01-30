from os import environ

import click

from IPython import embed

from inreach_ground_control.forecast import Forecast
from inreach_ground_control.weatherman import Weatherman

API_KEY = environ["DARK_SKY_API_KEY"]

@click.command()
@click.option('--latitude', help='degrees latitude in decimal form')
@click.option('--longitude', help='degrees longitude in decimal form')
def cli(latitude, longitude):
    click.echo(f"Sending forecast for {latitude}, {longitude} to Andrew!")

    forecast = Forecast(API_KEY, latitude=latitude, longitude=longitude)

    click.echo(f"Would send PUT request to {Weatherman(forecast).put_url()}")
