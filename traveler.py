import datetime
from flask import Flask
from flask import render_template
from werkzeug.contrib.cache import FileSystemCache
from forecastiopy import *

application = Flask(__name__)


def weather_data(latitude, longitude):
    cache = FileSystemCache('./cache')
    cache_key = '{}.{}'.format(latitude, longitude)
    data = cache.get(cache_key)
    if data is None:
        apikey = '3a4c7bb6f812d00b3bb9d19ceace7222'
        fio = ForecastIO.ForecastIO(apikey,
                                    units=ForecastIO.ForecastIO.UNITS_SI,
                                    lang=ForecastIO.ForecastIO.LANG_ENGLISH,
                                    latitude=latitude, longitude=longitude)

        currently = fio.currently
        data = currently
        cache.set(cache_key, data, timeout=300)  # 5 minutes
    return data


@application.route('/')
def index():
    past_trips = (
        {'latitude': 6.9319400, 'longitude': 79.8477800,
         'state': 'Srí Lanka', 'city': 'Colombo',
         'date': datetime.date(2016, 12, 16)},
        {'latitude': 41.390205, 'longitude': 2.154007,
         'state': 'Spain', 'city': 'Barcelona',
         'date': datetime.date(2017, 4, 23)},
        {'latitude': 52.3740300, 'longitude': 4.8896900,
         'state': 'Netherlands', 'city': 'Amsterdam',
         'date': datetime.date(2017, 6, 1)},
        {'latitude': 64.133333, 'longitude': -21.933333,
         'state': 'Iceland', 'city': 'Reykjavik',
         'date': datetime.date(2017, 9, 20)},
        {'latitude': 3.139003, 'longitude': 101.686855,
         'state': 'Malaysia', 'city': 'Kualalumpur',
         'date': datetime.date(2017, 12, 13)},
    )
    current_trip = {'latitude': 35.917973, 'longitude': 14.409943,
                    'state': 'Malta', 'city': 'Birgu',
                    'date': datetime.date(2018, 2, 28)}

    state = current_trip['state']
    city = current_trip['city']
    started_at = current_trip['date'].strftime('%Y/%m/%d')

    data = weather_data(current_trip['latitude'], current_trip['longitude'])

    temperature = data['temperature']
    summary = data['summary']
    context = {'temperature': temperature, 'summary': summary,
               'state': state, 'city': city, 'started_at': started_at}
    return render_template('index.html', **context)


if __name__ == '__main__':
    application.run()
