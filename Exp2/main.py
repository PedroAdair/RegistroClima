from func import *
import schedule

duracionDia = 5 #minutos
schedule.every(duracionDia).minutes.do(print,'------------------------------------------')
schedule.every(duracionDia).minutes.do(message_email)

while True:
    
    schedule.run_pending()
