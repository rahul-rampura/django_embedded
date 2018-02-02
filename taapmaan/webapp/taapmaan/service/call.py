import requests
from requests.exceptions import ConnectionError

from service.logger import log


def get_reading(server_ip, sensor_url, sensor_obj):
    """Get reading of a sensor

    Args:
        server_ip: Server IP address/hostname
        sensor_url: Sensor's URL to GET reading
        sensor_obj: Instance of sensor. Sensor.objects.get(name='<name>')

    Returns:
        Reading as a float value

    Raises:
        Exception, if failed to GET a reading
    """
    print "[DEBUG] service.call.get_reading ", server_ip, sensor_url, sensor_obj
    #return float(31.23)
    #import random
    #return float(random.randint(30,40))
    # Build URL
    if sensor_url[0] == '/':
        url = 'http://' + server_ip + sensor_url
    else:
        url = 'http://' + server_ip + '/' + sensor_url

    # Get reading
    try:
        data = requests.get(url)
        print data
    except ConnectionError as e:
        msg = 'Failed to connect. Reason - [%s]' % e
        log(level='ERROR', sensor=sensor_obj.name, message=msg)
	return None
        #raise Exception('Failed to GET %s' % url)

    # Process reading and return accordingly
    if data.ok:
        msg = 'Got reading [%s]' % data.text
        log(level='INFO', sensor=sensor_obj.name, message=msg)
	try:
            return float(data.text.split(' ')[0])
	except:
	    pass
    else:
        msg = 'Failed to get reading'
        log(level='ERROR', sensor=sensor_obj.name, message=msg)
        #raise Exception('Failed to GET %s' % url)

    return None        

def get_cooler_status(server_ip, sensor_url, sensor_obj):
    """Get cooler status (On/Off)

    Args:
        server_ip: Server IP address/hostname
        sensor_url: Cooler's URL to GET reading
        sensor_obj: Instance of sensor. Sensor.objects.get(name='<name>')

    Returns:
        Reading as a float value

    Raises:
        Exception, if failed to GET a reading
    """
    print "[DEBUG] service.call.get_cooler_status", server_ip, sensor_url, sensor_obj
    if sensor_url[0] == '/':
        url = 'http://' + server_ip + sensor_url
    else:
        url = 'http://' + server_ip + '/' + sensor_url

    # Get reading
    try:
        data = requests.get(url)
    except ConnectionError as e:
        msg = 'Failed to connect. Reason - [%s]' % e
        log(level='ERROR', sensor=sensor_obj.name, message=msg)
        #raise Exception('Failed to GET %s' % url)

    # Process reading and return accordingly
    if data.ok:
        msg = 'Status of cooler [%s]' % data.text
        log(level='INFO', sensor=sensor_obj.name, message=msg)
        if data.text.split(' ')[0] == 'ON':
            return True
        return False
    else:
        msg = 'Failed to get status of cooler'
        log(level='ERROR', sensor=sensor_obj.name, message=msg)
        #raise Exception('Failed to GET %s' % url)

def stop_cooler(server_ip, sensor_url='/device/power/cooler/OFF'):
    """Stop cooler

    Args:
        server_ip: Server IP address/hostname
        sensor_url: Cooler's URL to GET reading
        sensor_obj: Instance of sensor. Sensor.objects.get(name='<name>')

    Returns:
        True, if operation is successful
        False, if operation fails
    """
    print "[DEBUG] service.call.stop_cooler", server_ip, sensor_url
    if sensor_url[0] == '/':
        url = 'http://' + server_ip + sensor_url
    else:
        url = 'http://' + server_ip + '/' + sensor_url

    # Post request
    try:
        data = requests.post(url)
    except ConnectionError as e:
        msg = 'Failed to connect cooler. Reason - [%s]' % e
        log(level='ERROR', message=msg)

    if data.ok:
        msg = 'Cooler swicthed OFF'
        log(level='INFO', message=msg)
        return True
    else:
        return False

def start_cooler(server_ip, sensor_url='/device/power/cooler/ON'):
    """Stop cooler

    Args:
        server_ip: Server IP address/hostname
        sensor_url: Cooler's URL to GET reading
        sensor_obj: Instance of sensor. Sensor.objects.get(name='<name>')

    Returns:
        True, if operation is successful
        False, if operation fails
    """
    print "[DEBUG] service.call.stop_cooler", server_ip, sensor_url
    if sensor_url[0] == '/':
        url = 'http://' + server_ip + sensor_url
    else:
        url = 'http://' + server_ip + '/' + sensor_url

    # Post request
    try:
        data = requests.post(url)
    except ConnectionError as e:
        msg = 'Failed to connect cooler. Reason - [%s]' % e
        log(level='ERROR', message=msg)

    if data.ok:
        msg = 'Cooler swicthed ON'
        log(level='INFO', message=msg)
        return True
    else:
        return False       
