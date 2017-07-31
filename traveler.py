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

    prague = [50.0880400, 14.4207600]
    colombo = [6.9319400, 79.8477800]
    dublin = [53.350140,  -6.266155]
    barcelona = [41.390205,  2.154007]
    amsterdam = [52.3740300,  4.8896900]
    reykjavik = [64.133333, -21.933333]

    current = reykjavik

    state = 'Iceland'
    city = 'Reykjavík'
    started_at = '2017/09/20'

    data = weather_data(*current)

    temperature = data['temperature']
    summary = data['summary']
    context = {'temperature': temperature, 'summary': summary,
               'state': state, 'city': city, 'started_at': started_at}
    return render_template('index.html', **context)


@application.route('/xoxo/')
def xoxo():

    coordinates = [10.762622, 106.660172]

    data = weather_data(*coordinates)

    temperature = data['temperature']
    summary = data['summary']
    context = {'temperature': temperature, 'summary': summary}
    return render_template('xoxo.html', **context)


if __name__ == '__main__':
    application.run()
