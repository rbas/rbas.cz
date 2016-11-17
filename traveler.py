from flask import Flask
from flask import render_template
from werkzeug.contrib.cache import FileSystemCache
from forecastiopy import *

application = Flask(__name__)


def weather_data(latitude, longitude):
    cache = FileSystemCache('./')
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
        cache.set(cache_key, data, timeout=3600)
    return data


@application.route('/')
def index():

    prague = [50.0880400, 14.4207600]
    colombo = [6.9319400, 79.8477800]

    data = weather_data(*colombo)

    temperature = data['temperature']
    summary = data['summary']
    context = {'temperature': temperature, 'summary': summary}
    return render_template('index.html', **context)


if __name__ == '__main__':
    application.run()
