import os
import subprocess
import time
import tarfile
from datetime import datetime
from threading import Timer
import logging
import sys

minecraft_dir = "F:/home/xangma/MCSERVER/survival"
backup_dir = "Z:/MCSERVER_WORLD1"
executable = 'java -Xmx2048m -XX:+UseConcMarkSweepGC -jar "%s/spigot-1.12.2.jar"' %minecraft_dir
exclude_file = "plugins/dynmap"

logname = minecraft_dir + '/' + 'MCSERVER.log'
file_handler = logging.FileHandler(filename=logname)
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(
    level=logging.DEBUG, 
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=handlers
)

logger = logging.getLogger('MCLOG')
logging.info('Logname: %s' %logname)

def server_command(cmd):
    logging.info('Writing server command')
    process.stdin.write(str.encode('%s\n' %cmd)) #just write the command to the input stream
    process.stdin.flush()

def server_start():
    os.chdir(minecraft_dir)
    logging.info('Starting server')
    process = subprocess.Popen(executable, stdin=subprocess.PIPE)
    logging.info("Server started.")
    return process

def filter_function(tarinfo):
     if tarinfo.name != exclude_file:
          logging.info(tarinfo.name,"ADDED")
          return tarinfo

def make_tarfile(output_filename, source_dir):
    logging.info('Making tarfile')
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir),filter=filter_function)

def backup():
    global t
    server_command("say Backup starting. World no longer saving...")
    server_command("save-off")
    server_command("save-all")
    time.sleep(3)
    os.chdir(backup_dir)
    logging.info('Deleting last file')
    try:
        os.remove("%s\\minecraft-hour24.tar.gz"%backup_dir)
    except:
        pass
    logging.info('Renaming old files')
    for i in range(24,0,-1):
        try:
            os.rename("%s\\minecraft-hour%s.tar.gz"%(backup_dir,i-1), "%s\\minecraft-hour%s.tar.gz" %(backup_dir,i))
        except:
            pass
    make_tarfile("%s\\minecraft-hour0.tar.gz"%backup_dir, minecraft_dir+"/")
    server_command("save-on")
    server_command("say Backup complete. World now saving. ")
    logging.info('Starting new timer')
    try:
        t = Timer(next_backuptime(), backup) # FIND NEXT HOURLY MARK
        t.start() # START BACKUP FOR THEN
        logging.info('New timer started')
    except:
        logging.info('',exc_info=True)
        os.popen('TASKKILL /PID '+str(process.pid)+' /F')

def next_backuptime():
    logging.info('Calculating next time')
    x=datetime.today()
    if x.hour != 23:
        y=x.replace(hour=x.hour+1, minute=0, second=0, microsecond=0)
    else:
        try:
            y=x.replace(day=x.day+1,hour=0,minute=0,second=0,microsecond=0)
        except:
            try:
                y=x.replace(month=x.month+1,day=1,hour=0,minute=0,second=0,microsecond=0)
            except:
                try:
                    y=x.replace(year=x.year+1,month=1,day=1,hour=0,minute=0,second=0,microsecond=0)
                except:
                    logging.info('I, the backup script, have no idea what time it is in an hour.',exc_info=True)
                    os.popen('TASKKILL /PID '+str(process.pid)+' /F')
    logging.info('Next backup time is %s' %y)
    delta_t=y-x
    secs=delta_t.seconds+1
    return secs

process=server_start() # START SERVER
time.sleep(60) # WAIT FOR IT TO START

logging.info('Starting backup timer')
try:
    t = Timer(next_backuptime(), backup) # FIND NEXT HOURLY MARK
    t.start() # START BACKUP FOR THEN
    logging.info('Timer started')
except:
    logging.info('',exc_info=True)
    os.popen('TASKKILL /PID '+str(process.pid)+' /F')
