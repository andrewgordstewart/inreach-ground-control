import collections

import pytest
import pytest_mock

from inreach_ground_control.message import Message

DEFAULT_LATITUDE = 42
DEFAULT_LONGITUDE = 45

def message_factory(text_msg="wx +2 days\ndaily=YES\nhourly=n\nunits=aUto\ninclude_emoji=True"):
    return Message(
        text_msg_extid="id-number-1",
        text_msg=text_msg,
        latitude=DEFAULT_LATITUDE,
        longitude=DEFAULT_LONGITUDE,
        response_sent=False
    )

@pytest.fixture
def message():
    return message_factory()

def test_query_params_type(message):
    assert type(message.query_params()) == collections.defaultdict

def test_first_line_requirements(message):
    with pytest.raises(AssertionError):
        Message(
            text_msg_extid="id-number-1",
            text_msg="invalid first line",
            latitude=42,
            longitude=-43,
            response_sent=False
        )

@pytest.mark.parametrize("text_msg,latitude,longitude", [
    ("wx +2 days\nlatitude=3.1415\nlongitude=55", 3.1415, 55),
    ("wx +2 days\nlatitude=-43.2\nlongitude=55", -43.2, 55),
    ("wx +2 days\nlatitude=-5", DEFAULT_LATITUDE, DEFAULT_LONGITUDE),
    ("wx +2 days\nlongitude=-5", DEFAULT_LATITUDE, DEFAULT_LONGITUDE),
    ("wx +2 days\ndaily=FALSE", DEFAULT_LATITUDE, DEFAULT_LONGITUDE)
])

def test_coordinates(message, text_msg, latitude, longitude):
    message.text_msg = text_msg
    opts = message.query_params()

    assert opts["latitude"] == latitude
    assert opts["longitude"] == longitude

@pytest.mark.parametrize("text_msg,start_offset_days", [
    ("wx +2 days\ndaily=YES", 2),
    ("wx -1 days\ndaily=YES", -1),
    ("wx now\ndaily=YES", 0)
])

def test_start_offset_days(message, text_msg, start_offset_days):
    message.text_msg = text_msg
    opts = message.query_params()

    assert opts["start_offset_days"] == start_offset_days

@pytest.mark.parametrize("text_msg,daily,hourly", [
    ("wx +2 days\ndaily=YES\nhourly=n", True, False),
    ("wx -1 days\ndaily=true\nhourly=f", True, False),
    ("wx now\ndaily=t", True, None)
])
def test_boolean_options(message, text_msg, daily, hourly):
    message.text_msg = text_msg
    opts = message.query_params()

    assert opts["daily"] is daily
    assert opts["hourly"] is hourly

@pytest.mark.parametrize("text_msg,units", [
    ("wx +2 days\nunits=auto", "auto"),
    ("wx +2 days\nunits=aUto", "auto")
])
def test_units(message, text_msg, units):
    # opts["units"] should be lowercased
    message.text_msg = text_msg
    opts = message.query_params()

    assert opts["units"] == 'auto'

def test_invalid_keys(message):
    opts = message.query_params()

    # Invalid keys should be ignored
    assert opts["include_emoji"] == None
