from django.contrib import admin

# Register your models here.

from models import Log
from models import Mail
from models import Sensor
from models import SensorData
from models import Rule
from models import Server
from models import Device

admin.site.register(Sensor)
admin.site.register(Log)
admin.site.register(Mail)
admin.site.register(SensorData)
admin.site.register(Rule)
admin.site.register(Server)
admin.site.register(Device)
