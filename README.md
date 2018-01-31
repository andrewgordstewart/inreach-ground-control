## inreach-ground-control
An app for reading and responding to messages from an inReach satellite messenger.

Heavily inspired by [wx2inreach](https://wx2inreach.weebly.com/), which, while
excellent, does not include raw meterological information -- notably, wind speed
and atmospheric pressure -- that can be crucial pieces of information when
planning in the field.

## Disclaimer

This service was developed almost entirely as a learning exercise.
Currently,  bare minimum functionality has been implemented to be able to tell me
how windy it may be in the mountains in Patagonia.

If you would like to test this in the field, please contact me and I will
give you further instructions on how to contact my server.
However, there is no warranty or guarantee that the service will work,
or will provide an accurate forecast.

## Usage
`WeatherReport.report_weather()` will monitor a specified email inbox, and
respond to requests for weather forecasts _only for messages that were sent
from an inReach device_.

Forecasts are generously provided by the [Dark Sky](https://darksky.net/dev/docs)
API.

Every request for a message must begin with `wx <start_time>`, where `start_time`
is either `now` or `+n days`.

The simplest message that will be answered is, as with wx2inreach, 'wx now'.
The service will respond with a "daily" weather report for your current location
(inferred by the inReach message) for today and the following two days.

By default, the units will be automatically be inferred from your current country.
This may be overwritten by setting the `units` parameter.

### Options
- Options should be separated by commas.
- All whitespace (spaces and new lines) are ignored -- all options may be specified
  on one line, as long as they are separated by commas.
- Options not listed below are currently ignored -- you may set `loc=My House`,
  for instance, to identify a location.
- Both lat and lon must be present -- otherwise, they will be ignored, and the
  user's location is used.
- See https://darksky.net/dev/docs for details about the units option.


In other words, messages should look like so, with lines 2-5 optional.
```
wx <time>,
lat=<decimal latitude coordinate>,
lon=<decimal longitude coordinate>,
days=<integer between 1 and 10>,
units=<auto,ca,uk2,us,si>
```

### Example responses
TODO

## TODO
- Hourly forecasts
- Repeating forecasts
- Weather summary
