from func import *
import schedule

duracionDia = 1 #minutos
schedule.every(duracionDia).minutes.do(print,'------------------------------------------')
schedule.every(duracionDia).minutes.do(message_email)

while True:
    
    schedule.run_pending()
