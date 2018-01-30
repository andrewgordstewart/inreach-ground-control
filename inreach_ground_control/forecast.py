from os import environ

from forecastiopy import ForecastIO, FIOCurrently, FIOHourly, FIODaily

API_KEY = environ["DARK_SKY_API_KEY"]

class Forecast(ForecastIO.ForecastIO):
    """
    Calls the Darksky API.
    Parses response based on forecast params.
    """

    def __init__(self, *args, **kwargs):
        super(Forecast, self ).__init__(*args, **kwargs)

        self.current_forecast = FIOCurrently.FIOCurrently(self)
        self.hourly_forecast =  FIOHourly.FIOHourly(self)
        self.daily_forecast =  FIODaily.FIODaily(self)

    def current_report(current_forecast):
        # Current

        # Don't use characters on useless precision!
        return (
            "hPa:{int(current_forecast.pressure)}/"
            "spd:{int(current_forecast.windSpeed)}/"
            "gst:{int(current_forecast.windGust)}/"
            "wbr:{int(current_forecast.windBearing)}/"
            "tmp:{int(current_forecast.temperature)}/"
            "pc%:{int(current_forecast.precipProbability)}"
            "pci:{int(current_forecast.precipIntensity)}"
        )

    def daily_report(self, days=3, start_offset_days=0):
        daily_forecast = self.daily_forecast
        def get_series(df, key):
            shorten = lambda s: str(int(s))
            return ",".join(shorten(d[key]) for d in df.data[start_offset_days:start_offset_days + days])

        wind_speed = zip(
            get_series(daily_forecast, "windSpeed").split(','),
            get_series(daily_forecast, "windGust").split(',')
        )
        wind_speed = ",".join([speed + '-' + gust for speed, gust in wind_speed])

        report = (
            """
                start:+{start_offset_days} days
                hPa:{pressure}
                wnd:{windSpeed}
                wbr:{windBearing}
                hi:{temperatureHigh}
                low:{temperatureLow}
                pci:{precipIntensity}
                pc%:{precipProbability}
            """.format(**{
                "start_offset_days": start_offset_days,
                "pressure":          get_series(daily_forecast, "pressure"),
                "windSpeed":         wind_speed,
                "windBearing":       get_series(daily_forecast, "windBearing"),
                "temperatureHigh":   get_series(daily_forecast, "temperatureHigh"),
                "temperatureLow":    get_series(daily_forecast, "temperatureLow"),
                "precipIntensity":   get_series(daily_forecast, "precipIntensity"),
                "precipProbability": get_series(daily_forecast, "precipProbability")
            })
        )

        # Strip whitespace.
        report = ''.join(report.split())

        return report

if __name__ == "__main__":
    latitude = -49.291532
    longitude = -73.061839
    import IPython
    IPython.embed()
    niponino = Forecast(API_KEY, latitude=latitude, longitude=longitude)
