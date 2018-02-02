from mainpage.models import Log
from mainpage.models import Sensor


def log(level='DEBUG', sensor=None, message=''):
    """Log message in database

    Args:
        level: Log level
        sensor: Sensor name
        message: Message to be logged
    """
    if not sensor:
        sensor = 'webapp'
    sensor = Sensor.objects.get(name=sensor)
    log = Log(level=level, sensor=sensor, message=message)
    log.save()

def _log(level, sensor, message):
    """
    """
    log = Log(level=level, sensor=sensor, message=message)
    log.save()
