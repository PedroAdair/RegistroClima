import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import yaml
import logging


logging.basicConfig(filename='log.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

def message_email(mensaje: str, destinatarios:list):
    user = 'Constanza'
    asunto = 'Mensaje clima'

    msg = MIMEMultipart()
    msg['From']= user
    msg['Subject']= asunto
    msg['To']=  ', '.join(destinatarios)
    msg.attach(MIMEText(mensaje))
    with smtplib.SMTP('smtp.gmail.com') as server:
            server.starttls()
            server.login(config['USER_MAIL'], config['pw'])
            server.sendmail(config['USER_MAIL'],destinatarios, msg.as_string())