from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
import smtplib

from logger import log

def send_welcome_mail(mail_address):
    """ Send welcome mail to newly registered subscriber

    Args:
        mail_address: Email address of subscriber

    Raises:
        Raises <??>, if failed to send mail
    """
    from_email = "rahul.rampura@coriolis.co.in"
    to = mail_address

    subject = "[TAAPMAAN] Welcome to Taapmaan"
    text_content = ""
    html_content = "Thanks for subscribing to <b><a href='http://127.0.0.1:8000'>Taapmaan</a></b> web application."
    html_content += "<hr><br>"
    html_content += "<ul>1. You will be receiving weekly report on server room's "
    html_content += "temperature.</ul>"
    html_content += "<ul>2. ...</ul>"
    html_content += "<br><br>"
    html_content += "<hr>"
    html_content += "To unsubscribe, please <a href='http://127.0.0.1:8000/settings/webapp?unsubscribe=%s'>click here</a>." % mail_address

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    message = 'Sent welcome mail to [%s]' % mail_address
    log(level='INFO', sensor='webapp', message=message)

def send_unsubscribe_mail(mail_address):
    """ Send unsubscribe mail to registered subscriber

    Args:
        mail_address: Email address of subscriber

    Raises:
        Raises <??>, if failed to send mail
    """
    from_email = "rahul.rampura@coriolis.co.in"
    to = mail_address

    subject = "[TAAPMAAN] Successfully unsubscribed from Taapmaan webapp"
    text_content = ""
    html_content = "You have successfully unsubscribed from <b><a href='http://127.0.0.1:8000'>Taapmaan</a></b> web application."
    html_content += "<br>"
    html_content += "To subscribe again, please register your email address <a href='http://127.0.0.1:8000/settings/webapp'>here</a>."

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    message = 'Sent unsubscribe mail to [%s]' % mail_address
    log(level='INFO', sensor='webapp', message=message)

def send_notification(mail_address):
    """ Send notification

    Args:
        mail_address: List of email addresses

    Raises:
        Raises <??>, if failed to send mail
    """
    from django.core.mail import EmailMultiAlternatives

    from_email = "rahul.rampura@coriolis.co.in"
    to = mail_address

    subject = "[TAAPMAAN] Alert Notification"
    text_content = ""
    html_content = "Thanks for subscribing to <b><a href='http://127.0.0.1:8000'>Taapmaan</a></b> web application."
    html_content += "<hr><br>"
    html_content += "<ul>1. Temperature in server room just crossed the threshold "
    html_content += "value .</ul>"
    html_content += "<ul>2. Please check if AC in the server room is functioning properly.</ul>"
    html_content += "<br><br>"
    html_content += "<hr>"
    html_content += "To unsubscribe, please <a href='http://127.0.0.1:8000'>click here</a>."

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    message = 'Sent alert notification to [%s]' % mail_address
    log(level='INFO', sensor='webapp', message=message)
