import json
from os import environ, path
from datetime import datetime

from database import db_session
from digest import Digester
from forecast import Forecast
from message import Message
from weatherman import Weatherman

def report_weather():
    log('Checking emails.')
    Digester(
        db_session(),
        host=environ['INREACH_MAIL_HOST'],
        username=environ['INREACH_MAIL_USERNAME'],
        password=environ['INREACH_MAIL_PASSWORD']
    ).check_emails()
    messages = db_session.query(Message).filter(Message.response_sent == False).all()

    if environ['INREACH_RESPOND_TO_MESSAGES'] == 'YES':
        for message in messages:
            log(f'Responding to {message.text_msg_extid} @ {message.latitude}, {message.longitude}')

            query_params = message.query_params()

            response = Weatherman(message).send_forecast()

            if response.status_code == 200 and json.loads(response.text)['Success'] is True:
                # NB: json.loads may throw an error when the POST request was unsuccessful,
                # since inreach.garmin.com returns an html "Error page", along with status code 200.
                message.response_sent = True
                db_session.commit()
                log('Response sent.')
    else:
        log(f'Not responding to new emails.')

    db_session.remove()

def log(statement):
    filename = f'{path.expanduser("~")}/logs/weather_report.log'
    with open(filename, 'a+') as f:
        f.write(f'{datetime.now()} -- {statement}\n')

    return True

if __name__ == '__main__':
    report_weather()
