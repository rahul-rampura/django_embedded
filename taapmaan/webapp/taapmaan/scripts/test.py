import datetime
import django
import os
from os.path import abspath, dirname, join
import sys
import time
import threading

sys.path.insert(0, abspath(join(dirname(__file__), '../')))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "taapmaan.settings")
django.setup()

from mainpage.models import Sensor
from mainpage.models import SensorData
from mainpage.models import Server
from mainpage.models import Rule

from service import call
from service import operations
from service.logger import log


def rule_application(sensor):
    """
    Execute operation if any rule being satisfied
    """
    rules = Rule.objects.filter(sensor=sensor)

    # Calculate average
    for rule in rules:
        count = int(rule.retrospect_period/sensor.time_period)
        average = sum([x.value for x in SensorData.objects.filter(sensor=sensor.name)[:count]])/count

        #if rule.threshold <= average:
        if getattr(average, rule.position)(rule.threshold):
            print "rule satisfied"
            # Log rule satisfied
            message = 'Threshold crossed. Current average [%s]' % average
            log(level='CRITICAL', sensor='webapp', message=message)

            # Execute registered operation, only if rule is inactive.
            if rule.status != 'Active':
                # Execute operation
                getattr(operations, rule.operation)()

                # Mark rule as Active
                rule.status = 'ACTIVE'
                rule.save()

                # Mark opposite rule as "Inactive"
                # Example: If stop_fan is "active", then start_fan needs to be
                # marked as "Inactive"


                # send_notification

def sensor_application(*args):
    """
    1. Fetch reading depending on time period
    2. Execute operation, if any, depending any rule registered with
         specific sensor
    """
    sensor = args[0]

    reading = {}
    server_ip = Server.objects.get(pk=1).ip
    sensor_url = sensor.uri
    sensor = sensor
    while 1:
        # Fetch reading
        import pdb; pdb.set_trace()
        reading = call.get_reading(server_ip, sensor_url, sensor)
        #dt = datetime.datetime.now()
        from django.utils import timezone
        dt = timezone.localtime(timezone.now())
        #from django.utils import timezone
        #dt = timezone.now()

        # Save reading
        SensorData(time=dt, sensor=sensor, value=reading).save()
        return 0

        # Log message
        message = 'Saved reading [%s] at [%s]' % (reading, dt) 
        log(level='INFO', sensor=sensor.name, message=message)

        # Check rule book and execute operation accordingly
        rule_application(sensor)

        # Wait for next fetch
        time.sleep(sensor.time_period * 60)


def start_backend_application():
    """
    1. Create Thread/sensor
        1.1. Fetch reading depending on time period
        1.2. Execute operation, if any, depending any rule registered with
             specific sensor
    """
    sensors = Sensor.objects.filter(sensor_type='temperature')
    #if not isinstance(sensors, list):
    #    sensors = [sensors]

    for sensor in sensors:
        sensor_application((sensor))
        #rule_application(sensor)
    return 0

    threads = []
    for sensor in sensors:
        threadx = threading.Thread(target=sensor_application, args=(sensor, ))
        threads.append(threadx)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


def main():
    import pdb; pdb.set_trace()
    #dt = datetime.datetime.now()
    #from django.utils import timezone
    #dt = timezone.localtime(timezone.now())
    #import timezone
    #print timezone.now()
    #start_backend_application()
    #data = call.get_cooler_status('192.168.100.101', '/device/status/cooler', Sensor.objects.filter(sensor_type='webapp')[0])
    #data = call.stop_cooler('192.168.100.101')
    data = call.start_cooler('192.168.100.101')
    print data


if __name__ == '__main__':
    main()
    #from service import mail
    #mail.send_welcome_mail('madhav.mahajan@coriolis.co.in')
