from crontab import CronTab
from pathlib import Path

filename='Video-all-regions-num.py'
cron = CronTab(user=True)
job = cron.new(command=str(str("cd ")+ str(Path.cwd())+str(" && ")+str('/usr/bin/python3 '+ str(Path.cwd())+'/'+filename)))
job.hour.every(10)
cron.write()


filename='Video-all-regions-obitos.py'
cron = CronTab(user=True)
job = cron.new(command=str(str("cd ")+ str(Path.cwd())+str(" && ")+str('/usr/bin/python3 '+ str(Path.cwd())+'/'+filename)))
job.hour.every(10)
cron.write()
