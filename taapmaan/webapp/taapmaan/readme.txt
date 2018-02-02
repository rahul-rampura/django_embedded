Software,
1. Python 2.7.12
2. Django 1.10
3. Requests
4. pytz
5. django-smtp-ssl

To-do,
1. DONE - Title per template or view
2. Pagination using paginator module
3. Pagination update in javascript
4. Form to update rules and sensor information
5. Add another server for controlling fan
6. Checkin code
7. Favicon
8. Change name of index.html to plot.html
9. Change app name 'mainpage' to 'webapp'

Runing server,
1. running script, ssh -n -f root@10.11.9.197 "nohup /home/taapmaan/webapp/taapmaan/scripts/script.sh > /dev/null 2>&1 &"
2. running runserver, ssh -n -f root@10.11.9.197 "nohup /home/taapmaan/webapp/taapmaan/runserver.sh > /dev/null 2>&1 &"

URLs,
http://127.0.0.1:8000/?sensor=sensor1&start_date=2017-04-25T01:02:03&end_date=2017-04-26T04:05:06

Calling URL,
import requests
data = requests.get('http://192.168.100.103/temp/one')
check data.status_code == 200
reading = data.content or data.text


Running on Apache,
1. sudo chown :www-data taapmaan
2. sudo chown :www-data db.sqlite3
3. taapmaan/taapmaan/wsgi.py
4. sudo systemctl start apache2.service


Setup up DB,
1. Set models.Server with ip = 192.168.100.102
2. Set models.Sensor with webapp, webapp, description, ''
3. Set models.Scheduler with 5, 35, Mean, 15 
    sqlite> insert into mainpage_Scheduler values (1, 5, 35, 'Mean', 15);
4. Set models.GraphSetting with Annotation
5. Add cooler entry insert into mainpage_device values ('cooler1', 'cooler', 'Entrance cooler', '/device/status/cooler');


sql commands,
1. update row,
    update mainpage_sensor set uri='/sensor/temp/two' where (name='sensor2');
2. delete row,
    delete from mainpage_sensordata where (id=818);
3. Add cooler entry,
    insert into mainpage_device values ('cooler1', 'cooler', 'Entrance cooler', '/device/status/cooler');
4. Update server entry,
    update mainpage_server set device_ip='192.168.100.101' where (id=1);


To set up Google permission,
https://myaccount.google.com/lesssecureapps

curl -X GET http://192.168.100.103/sensor/temp/two
