"""Provides the weather forecast, and takes care of caching"""

# pylint: disable=C0103

import os
import errno
import logging
import urllib.request
from pathlib import Path
from datetime import datetime
import dateutil.parser
import untangle
from smarthome import settings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

XMLURL = settings.XMLWEATHERURL

def __ensure_path(path):
    """creates paths if they do not exist"""

    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def __get_weather():
    """Ensures that newest weather source is downloaded. Returns false if could not be downloaded"""

    def download_weather(path):
        """Downloads weather xml to file"""
        logger.info('Downloading weather data')

        response = urllib.request.urlopen(XMLURL)
        if response.code == 200:
            xml = response.read()
            untangledxml = untangle.parse(xml.decode('UTF-8')).weatherdata
            next_update = untangledxml.meta.nextupdate.cdata

            latestpath = os.path.join(path, 'latest.xml')
            nextupdatepath = os.path.join(path, 'nextupdate.txt')
            with open(latestpath, 'wb') as outfile,\
            open(nextupdatepath, 'wb') as nextupdatefile:
                outfile.write(xml)
                nextupdatefile.write(next_update.encode('UTF-8'))
            logger.info('Weather data downloaded successfully')
            return untangledxml
        else:
            logger.warning('weather XML returned code %i', response.code)
            return False

    logger.info('Running __get_weather()')

    scriptdir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(scriptdir, '.weathercache')
    __ensure_path(path)

    nextupdatepath = os.path.join(path, 'nextupdate.txt')
    if Path(nextupdatepath).is_file():
        with open(nextupdatepath, 'r') as nextupdatefile:
            date_in_file = dateutil.parser.parse(nextupdatefile.read())
            if date_in_file <= datetime.now():
                logger.info('Weather data is old')
                return download_weather(path)
            else:
                logger.info('Weather data was already up-to-date')
                latestpath = os.path.join(path, 'latest.xml')
                with open(latestpath, 'r') as cachedweather:
                    return untangle.parse(cachedweather.read()).weatherdata
    else:
        logger.info('nextupdate.txt does not exist')
        return download_weather(path)

def precipitation_in_interval(start, end):
    """Returns true if precipitation is likely in the given datetime interval"""
    untangledxml = __get_weather()

    if untangledxml != False:
        for hour in untangledxml.forecast.tabular.time:
            hourbegin = dateutil.parser.parse(hour['from'])
            # Check if this forecast data is inside start and end
            if hourbegin >= start and hourbegin < end:
                if float(hour.precipitation['value']) > 0:
                    return True
    return False

def wind_above_threshold_in_interval(start, end, threshold):
    """Returns true if wind speed is above or equal to the threshold (in m/s) in the given datetime interval"""
    untangledxml = __get_weather()

    if untangledxml != False:
        for hour in untangledxml.forecast.tabular.time:
            hourbegin = dateutil.parser.parse(hour['from'])
            # Check if this forecast data is inside start and end
            if hourbegin >= start and hourbegin < end:
                if float(hour.windSpeed['mps']) >= threshold:
                    return True
    return False

def temperature_below_threshold_in_interval(start, end, threshold):
    """Returns true temperature is below the threshold in the given datetime interval"""
    untangledxml = __get_weather()

    if untangledxml != False:
        for hour in untangledxml.forecast.tabular.time:
            hourbegin = dateutil.parser.parse(hour['from'])
            # Check if this forecast data is inside start and end
            if hourbegin >= start and hourbegin < end:
                if float(hour.temperature['value']) <= threshold:
                    return True
    return False
