from service.logger import log
import service.call
from mainpage.models import Server, Mail
import service.mail

def start_fan():
    device_ip = Server.objects.get(pk=1).device_ip
    service.call.start_cooler(device_ip, '/device/power/cooler/ON')
    msg = 'Fan started'
    #log(level='INFO', message=msg)

def stop_fan():
    device_ip = Server.objects.get(pk=1).device_ip
    service.call.stop_cooler(device_ip, '/device/power/cooler/OFF')
    msg = 'Fan stopped'
    #log(level='INFO', sensor='webapp', message=msg)


def send_mail():
    mailing_list = []
    emails = Mail.objects.all()
    for mail in emails:
        mailing_list.append(str(mail.email))
    msg = 'Mail sent'
    service.mail.send_notification(mailing_list)
    log(level='INFO', sensor='webapp', message=msg)

