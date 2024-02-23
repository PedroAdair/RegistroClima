import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import yaml
from func import *  

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

alerts = []
i = 0
for city in config['cities']:
    report = NotificationsAndWarmings(city, True)
    if report is not None:
        alerts.append(report)
        i +=1
user = 'Constanza'
asunto = 'Mensaje clima'
destinatarios = ['algebracimat2022@gmail.com']

mensaje = str(alerts)

msg = MIMEMultipart()
msg['From']= user
msg['Subject']= asunto
msg['To']=  ', '.join(destinatarios)
msg.attach(MIMEText(mensaje))
if len(mensaje)>0:
    with smtplib.SMTP('smtp.gmail.com') as server:
        server.starttls()
        server.login(config['USER_MAIL'], config['pw'])
        server.sendmail(config['USER_MAIL'],destinatarios, msg.as_string())

    print(f"hubo {i} incidentes, los cuales se reportaron a los siguientes correos: {', '.join(destinatarios)}")
