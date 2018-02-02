from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

import datetime
import json

from forms import GraphSettingForm
from forms import GraphPlotForm
from forms import SearchLogForm
from forms import EmailSettingForm
from forms import RuleForm
from forms import SensorForm
from models import Device
from models import GraphSetting
from models import Log
from models import Rule
from models import Sensor
from models import SensorData
from models import Server
from models import Mail
from service import call
from service.logger import log
from service import mail


def graph(request):
    sensors = []
    form_payload = {}
    template = 'index.html'
    #import pdb; pdb.set_trace()

    # Datetime format - YYYY-MM-DDTHH:MM:SS+HH:MM - ISO 8601 format
    # In out case, micro-second = 0, so format = YYYY-MM-DDTHH:MM:SS
    try:
        start_date = request.GET.get('start_date', '')
        start_time = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
        end_date = request.GET.get('end_date', '')
        end_time = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        # In case of invalid date or time or date-time format, show today's data
        start_time = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        end_time = datetime.datetime.combine(datetime.date.today(), datetime.time.max)

    form_payload['start_date'] = start_time
    form_payload['end_date'] = end_time

    # Adding time offset of +05:30. Need a solution here.
    start_time = start_time + datetime.timedelta(hours=5, minutes=30)
    end_time = end_time + datetime.timedelta(hours=5, minutes=30)

    #sensordata = SensorData.objects.all()
    try:
        sensor_name = request.GET['sensor']
        sensors_list = Sensor.objects.filter(name=sensor_name)
        form_payload['sensor'] = sensor_name
    except KeyError:
        sensors_list = Sensor.objects.filter(sensor_type='temperature')
        form_payload['sensor'] = 'All'

    for sensor in sensors_list:
        graph_data = []
        sensor_data = {}
        sensor_data['name'] = sensor.name

        sensordata = SensorData.objects.all()
        sensordata = sensordata.filter(
            sensor=Sensor.objects.filter(name=sensor.name),
            time__range=(start_time, end_time)
        )
        for data in sensordata:
            graph_data.append({
                'year' : int(data.time.strftime('%Y')),
                'month' : int(data.time.strftime('%m')),
                'day' : int(data.time.strftime('%d')),
                'hour' : int(data.time.strftime('%H')),
                'minute' : int(data.time.strftime('%M')),
                'second' : int(data.time.strftime('%S')),
                'value' : data.value,
                'sensor' : data.sensor.name,
            })
        sensor_data['data'] = json.dumps(graph_data)
        sensors.append(sensor_data)

    form = GraphPlotForm(form_payload)

    context = {
            'sensors' : sensors,
            'form' : form,
            'var' : 'variable data of home view',
        }
    return render(request, template, context)

def _mainpage(request):
    sensors = []
    template = 'index.html'

    #sensordata = SensorData.objects.all()

    for sensor in Sensor.objects.filter(sensor_type='temperature'):
        graph_data = []
        sensor_data = {}
        sensor_data['name'] = sensor.name

        sensordata = SensorData.objects.all()
        sensordata = sensordata.filter(sensor=Sensor.objects.filter(name=sensor.name)) 
        for data in sensordata:
            graph_data.append({
                'year' : int(data.time.strftime('%Y')),
                'month' : int(data.time.strftime('%m')),
                'day' : int(data.time.strftime('%d')),
                'hour' : int(data.time.strftime('%H')),
                'minute' : int(data.time.strftime('%M')),
                'second' : int(data.time.strftime('%S')),
                'value' : data.value,
                'sensor' : data.sensor.name,
            })
        sensor_data['data'] = json.dumps(graph_data)
        sensors.append(sensor_data)

    context = {
            'sensors' : sensors,
            'var' : 'variable data of home view',
        }
    return render(request, template, context)


@csrf_exempt
def logs(request):
    form_payload = {}
    count_per_page = 10
    template = 'logs.html'

    page = int(request.GET.get('page', 1))
    level = request.GET.get('level', '')
    sensor = request.GET.get('sensor', '')
    search_str = request.GET.get('search_str', '')

    logs = Log.objects.all()
    if level != 'All' and level != '':
        logs = logs.filter(level__iexact=level)
        form_payload['level'] = level
    if sensor != 'All' and sensor != '':
        logs = logs.filter(sensor__exact=sensor)
        form_payload['sensor'] = sensor
    if search_str != '':
        logs = logs.filter(message__icontains=search_str)
        form_payload['search_str'] = search_str

    p = Paginator(logs, count_per_page, request=request)
    pages = p.page(page)

    total = len(logs)
    start = (page - 1) * count_per_page
    end = page * count_per_page
    if end > total:
        end = total
    logs = logs[start:end]
    if total <= count_per_page:
        count_per_page = total
    try:
        total_pages = total/count_per_page
    except ZeroDivisionError:
        total_pages = 0

    form = SearchLogForm(form_payload)

    context = {
            'title' : 'Logs - Taapmaan',
            'logs' : logs,
            'form' : form,
	    'pages': pages,
            'pagination' : {
                'start' : start,
                'end' : end,
                'total' : total,
                'active_page' : page,
                'total_page' : range(1, total_pages+2),
            }
        }
    return render(request, template, context)

def sensor_settings(request):
    template = 'sensor_settings.html'
    latest_data = []
    devices = []

    # Server information
    sensor_info = Server.objects.get(pk=1)
    sensor_server_ip = sensor_info.sensor_ip
    device_server_ip = sensor_info.device_ip

    # Latest sensor reading
    sensordata = SensorData.objects.all()
    sensors = Sensor.objects.filter(sensor_type='temperature')
    for sensor in sensors:
        data = sensordata.filter(sensor=sensor).latest('time')
        latest_data.append({
            'name': sensor.name,
            'time': data.time + datetime.timedelta(hours=-5, minutes=-30),
            'reading': data.value,
        })

    # Device status
    devices = Device.objects.all()
    webapp = Sensor.objects.filter(sensor_type='webapp')[0]
    for device in devices:
        cooler_status = call.get_cooler_status(device_server_ip, device.uri, webapp)
        device.status = cooler_status

    if request.method == 'POST':
        new_sensor_form = SensorForm(request.POST)
        if new_sensor_form.is_valid():
            # Save new sensor information
            sensor = Sensor(
                    name=new_sensor_form.cleaned_data['name'],
                    sensor_type=new_sensor_form.cleaned_data['sensor_type'],
                    desc=new_sensor_form.cleaned_data['desc'],
                    uri=new_sensor_form.cleaned_data['uri'],
                    time_period=new_sensor_form.cleaned_data['time_period'],
                )
            sensor.save()

            # Log message
            message = 'Added new sensor [%s]' \
                % new_sensor_form.cleaned_data
            log(level='INFO', sensor='webapp', message=message)

            sensors = Sensor.objects.all()[1:]
            context = {
                    'title' : 'Sensor Settings - Taapmaan',
                    'sensors' : sensors,
                    'new_sensor_form' : new_sensor_form,
                    'latest_data' : latest_data,
                    'devices' : devices,
                    'var' : str(new_sensor_form.cleaned_data),
                }
            return render(request, template, context)
        else:
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++++"
            print "Form not valid...."

    new_sensor_form = SensorForm()
    sensors = Sensor.objects.all()[1:]

    context = {
            'title' : 'Sensor Settings - Taapmaan',
            'sensor_server' : sensor_server_ip,
            'sensors' : sensors,
            'new_sensor_form' : new_sensor_form,
            'latest_data' : latest_data,
            'device_server' : device_server_ip,
            'devices' : devices,
            'var' : 'variable data of sensor view',
        }
    return render(request, template, context)


def rule_settings(request):
    template = 'rule_settings.html'

    if request.method == 'POST':
        new_rule_form = RuleForm(request.POST)
        if new_rule_form.is_valid():
            # Save new rule information
            rule = Rule(
                    sensor=Sensor.objects.get(name=new_rule_form.cleaned_data['sensor']),
                    threshold=new_rule_form.cleaned_data['threshold'],
                    retrospect_period=new_rule_form.cleaned_data['retrospect_period'],
                    position=new_rule_form.cleaned_data['position'],
                    email=Mail.objects.get(email=new_rule_form.cleaned_data['email']),
                    operation=new_rule_form.cleaned_data['operation'],
                    status='INACTIVE',
                )
            rule.save()

            # Log message
            message = 'Added new rule [%s]' \
                % new_rule_form.cleaned_data
            log(level='INFO', sensor='webapp', message=message)

            rules = Rule.objects.all()
            context = {
                    'rules' : rules,
                    'new_rule_form' : new_rule_form,
                    'var' : str(new_rule_form.cleaned_data),
                }
            return render(request, template, context)
        else:
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++++"
            print "Form not valid...."

    new_rule_form = RuleForm()
    rules = Rule.objects.all()

    context = {
            'title' : 'Rules - Taapmaan',
            'rules' : rules,
            'new_rule_form' : new_rule_form,
            'var' : 'variable data of rule view',
        }
    return render(request, template, context)


def webapp_settings(request):
    message = ''
    template = 'webapp_settings.html'

    try:
        unsubscribe_email = request.GET['unsubscribe']
        try:
            email = Mail.objects.get(email=unsubscribe_email)
        except Mail.DoesNotExist:
            # Email address not found in database.
            pass
        else:
            email.delete()

            # Log message
            message = 'Unsubscribed Email address [%s]' % unsubscribe_email
            log(level='INFO', sensor='webapp', message=message)

            # Send unsubscribe email
            #mail.send_unsubscribe_mail(unsubscribe_email) 
    except KeyError:
        pass

    if request.method == 'POST':
        email_form = EmailSettingForm(request.POST)
        graph_setting_form = GraphSettingForm(request.POST)
        if email_form.is_valid():
            # Save email address
            email = Mail(email=email_form.cleaned_data['email'])
            email.save()

            # Send welcome email
            mail.send_welcome_mail(email_form.cleaned_data['email']) 
        
            # Log message
            message = 'Registered Email address [%s]' \
                % email_form.cleaned_data['email']
            log(level='INFO', sensor='webapp', message=message)

            emails = Mail.objects.all()
            context = {
                    'emails' : emails,
                    'email_setting_form' : email_form,
                    'graph_setting_form' : graph_setting_form,
                    'message' : message,
                    'var' : str(email_form.cleaned_data),
                }
            return render(request, template, context)
        elif graph_setting_form.is_valid():
            # Email form/Scheduler form is not valid. Might be a Graph Setting form
            setting = GraphSetting.objects.get(pk=1)
            setting.graph_type = graph_setting_form.cleaned_data['graph_type']
            setting.save()

            # Log message
            message = 'Graph settings changed to [%s]' \
                % graph_setting_form.cleaned_data
            log(level='INFO', sensor='webapp', message=message)

            emails = Mail.objects.all()
            context = {
                    'emails' : emails,
                    'email_setting_form' : email_form,
                    'graph_setting_form' : graph_setting_form,
                    'message' : message,
                    'var' : str(email_form.cleaned_data),
                }
            return render(request, template, context)
 
        else:
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++++"
            print "Form not valid...."

    email_form = EmailSettingForm()
    graph_setting_form = GraphSettingForm()
    emails = Mail.objects.all()

    context = {
            'title' : 'Application settings - Taapmaan',
            'emails' : emails,
            'email_setting_form' : email_form,
            'graph_setting_form' : graph_setting_form,
            'message' : message,
            'var' : 'variable data of settings view',
        }
    return render(request, template, context)


def about(request):
    template = 'about.html'

    context = {
            'title' : 'About - Taapmaan',
            'var' : 'variable data of about view',
        }
    return render(request, template, context)

def ajax_about(request):
    template = 'about.html'

    context = {
            'var' : 'variable data of about view',
        }
    return render(request, template, context)
