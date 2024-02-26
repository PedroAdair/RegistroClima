from func import *
import schedule

duracionDia = 15 #minutos
schedule.every(duracionDia).minutes.do(print,'------------------------------------------')
schedule.every(duracionDia).minutes.do(message_email)