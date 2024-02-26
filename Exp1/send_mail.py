import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import yaml
from func import *  
logging.basicConfig(filename='log.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)


def message_email():
    alerts = []
    i = 0
    for city in config['cities']:
        report = NotificationsAndWarmings(city, True)
        if report is not None:
            alerts.append(report)
            i +=1
    user = 'Constanza'
    asunto = 'Mensaje clima'
    destinatarios = ['ferphoenix1@gmail.com']

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

        text = f"hubo {i} incidentes"
        logging.warning(text)
