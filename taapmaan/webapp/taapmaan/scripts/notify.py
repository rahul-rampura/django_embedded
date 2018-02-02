import requests
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

r = requests.get("http://172.20.4.71/server/west/temp/one")
print r.content

server = smtplib.SMTP('smtp.gmail.com', 587)

server.starttls()
server.login("rahul.rampura@coriolis.co.in", "coriolis@1994")

text = "Westend Server Room Temp : " + r.content

send_from = "rahul.rampura@gmail.com"
send_to = 'rahul.rampura@gmail.com, rahulrampura@yahoo.com, rahul.rampura@coriolis.co.in'
subject = "Taapmaan Daily Update"
text = "Westend Server Room Temp : " + r.content

msg = MIMEMultipart()
msg['From'] = send_from
msg['To'] = send_to
msg['Date'] = formatdate(localtime=True)
msg['Subject'] = subject
msg.attach( MIMEText(text) )

server.sendmail(send_from, send_to, msg.as_string())

server.close()
