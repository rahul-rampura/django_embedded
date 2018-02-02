from django import forms
from django.db import utils

from models import ALGORITHMS
from models import GRAPH_TYPES
from models import LOGGING_LEVELS
from models import OPERATIONS
from models import POSITION_LEVELS
from models import SENSOR_TYPES
from models import SCHEDULER_TIME_PERIOD
from models import GraphSetting
from models import Mail
from models import Sensor


class GraphSettingForm(forms.Form):

    graph_type = forms.ChoiceField(choices=GRAPH_TYPES)

    def __init__(self, *args, **kwargs):
        super(GraphSettingForm, self).__init__(*args, **kwargs)
        try:
            setting = GraphSetting.objects.all()[0]
            self.fields['graph_type'].initial = setting.graph_type
        except utils.OperationalError:
            pass


class GraphPlotForm(forms.Form):

    def generate_sensor_choices():
        choices = [('All', 'All')]
        try:
            sensors = Sensor.objects.filter(sensor_type='temperature')
            for sensor in sensors:
                choices.append((sensor.name, sensor.name))

            return tuple(choices)
        except utils.OperationalError:
            return tuple(choices)

    sensor = forms.ChoiceField(choices=generate_sensor_choices(), required=False)
    start_date = forms.DateTimeField(input_formats='%Y-%m-%d %H:%M:%S', required=False)
    end_date = forms.DateTimeField(input_formats='%Y-%m-%d %H:%M:%S', required=False)


class SearchLogForm(forms.Form):

    def generate_sensor_choices():
        choices = [('All', 'All')]
        try:
            sensors = Sensor.objects.all()
            for sensor in sensors:
                choices.append((sensor.name, sensor.name))

            return tuple(choices)
        except utils.OperationalError:
            return tuple(choices)

    level = forms.ChoiceField(choices=LOGGING_LEVELS, required=False)
    sensor = forms.ChoiceField(choices=generate_sensor_choices(), required=False)
    search_str = forms.CharField(label='Search String', max_length=256, required=False)


class SensorForm(forms.Form):

    name = forms.CharField(help_text='...')
    sensor_type = forms.ChoiceField(choices=SENSOR_TYPES, help_text='...')
    desc = forms.CharField(help_text='...')
    uri = forms.CharField(help_text='...')
    time_period = forms.IntegerField()


class RuleForm(forms.Form):

    def generate_sensor_choices():
        choices = [('', '')]
        try:
            sensors = Sensor.objects.all()
            for sensor in sensors:
                choices.append((sensor.name, sensor.name))
            return tuple(choices)
        except utils.OperationalError:
            return tuple(choices)

    def generate_email_choices():
        choices = [('', '')]
        try:
            emails = Mail.objects.all()
            for email in emails:
                choices.append((email.email, email.email))
            return tuple(choices)
        except utils.OperationalError:
            return tuple(choices)

    sensor = forms.ChoiceField(choices=generate_sensor_choices())
    threshold = forms.IntegerField(
        help_text='Temperature threashold in Celsius')
    retrospect_period = forms.IntegerField(
        help_text='Consolidate last N readings to intiate any tasks')
    position = forms.ChoiceField(choices=POSITION_LEVELS)
    email = forms.ChoiceField(choices=generate_email_choices())
    operation = forms.ChoiceField(choices=OPERATIONS)


class EmailSettingForm(forms.Form):

    email = forms.EmailField(required=True)
