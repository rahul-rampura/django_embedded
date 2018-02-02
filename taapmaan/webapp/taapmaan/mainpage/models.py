from __future__ import unicode_literals

from django.db import models


GRAPH_TYPES = (
    ('LINE', 'Line'),
    ('ANNOTATION', 'Annotation'),
)

ALGORITHMS = (
    ('Average', 'Average'),
    ('Mean', 'Mean'),
    ('Meridian', 'Meridian'),
)

POSITION_LEVELS = (
    ('__lt__', 'less than'),
    ('__eq__', 'equal to'),
    ('__gt__', 'greater than'),
)

OPERATIONS = (
    ('stop_fan', 'Stop Fan'),
    ('start_fan', 'Start Fan'),
    ('send_mail', 'Send notification'),
)

RULE_STATUS = (
    ('ACTIVE', 'Active'),
    ('INACTIVE', 'Inactive'),
)

LOGGING_LEVELS = (
    ('All', 'All'),
    ('INFO', 'INFO'),
    ('DEBUG', 'DEBUG'),
    ('WARNING', 'WARNING'),
    ('CRITICAL', 'CRITICAL'),
    ('ERROR', 'ERROR'),
)

SENSOR_TYPES = (
    ('webapp', 'webapp'),
    ('temperature', 'temperature'),
    ('...', '...'),
)


SCHEDULER_TIME_PERIOD = 5
TEMPERATURE_THRESHOLD = 35
ALGORITHM_MEAN = 'Mean'
ALGORITHM_MERIDAN = 'Meridian'
DEFAULT_ALGORITHM = ALGORITHM_MEAN
SCHEDULER_RETROSPECT_PERIOD = '15'


class GraphSetting(models.Model):
    graph_type = models.CharField(max_length=64, choices=GRAPH_TYPES)

class Sensor(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    sensor_type = models.CharField(choices=SENSOR_TYPES, max_length=64)
    desc = models.CharField(max_length=265)
    uri = models.CharField(max_length=64, default='/temp/one')
    time_period = models.IntegerField(default=SCHEDULER_TIME_PERIOD)

    def __unicode__(self):
        return self.name


class Device(models.Model):
    DEVICE_TYPES = (
        ('cooler', 'cooler'),
    )

    name = models.CharField(max_length=64, primary_key=True)
    device_type = models.CharField(choices=DEVICE_TYPES, max_length=64)
    desc = models.CharField(max_length=265)
    uri = models.CharField(max_length=64, default='/device/status/cooler')

    def __unicode__(self):
        return self.name


class SensorData(models.Model):
    time = models.DateTimeField()
    sensor = models.ForeignKey(Sensor)
    value = models.FloatField()

    class Meta:
        ordering = ('-time' ,)

class Server(models.Model):
    sensor_ip = models.GenericIPAddressField()
    device_ip = models.GenericIPAddressField()


class Mail(models.Model):
    email = models.EmailField(max_length=254)

    def __unicode__(self):
        return self.email


class Rule(models.Model):
    sensor = models.ForeignKey(Sensor)
    threshold = models.IntegerField(default=TEMPERATURE_THRESHOLD)
    retrospect_period = models.IntegerField(default=SCHEDULER_RETROSPECT_PERIOD)
    position = models.CharField(max_length=16, choices=POSITION_LEVELS)
    email = models.ForeignKey(Mail)
    operation = models.CharField(max_length=128, choices=OPERATIONS)
    status = models.CharField(max_length=16, choices=RULE_STATUS)

    def __unicode__(self):
        return "{0} - Temperature {1} {2} - {3} - Status {4}".format(
        self.sensor, self.position, self.threshold, self.operation, self.status)


class Log(models.Model):
    time = models.DateTimeField(auto_now=True)
    level = models.CharField(max_length=5, choices=LOGGING_LEVELS)
    sensor = models.ForeignKey(Sensor)
    message = models.CharField(max_length=254)

    class Meta:
        ordering = ('-time' ,)

    def __unicode__(self):
        return "{0} {1} {2}".format(self.level, self.sensor, self.message)
