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
    process.stdin.write(str.encode('%s\n' %cmd)) #just write the command to the input stream
    process.stdin.flush()

def server_start():
    os.chdir(minecraft_dir)
    process = subprocess.Popen(executable, stdin=subprocess.PIPE)
    logging.info("Server started.")
    return process

def filter_function(tarinfo):
     if tarinfo.name != exclude_file:
          logging.info(tarinfo.name,"ADDED")
          return tarinfo

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir),filter=filter_function)

def backup():
    global t
    server_command("say Backup starting. World no longer saving...")
    server_command("save-off")
    server_command("save-all")
    time.sleep(3)
    os.chdir(backup_dir)
    try:
        os.remove("%s\\minecraft-hour24.tar.gz"%backup_dir)
    except:
        pass
    for i in range(24,0,-1):
        try:
            os.rename("%s\\minecraft-hour%s.tar.gz"%(backup_dir,i-1), "%s\\minecraft-hour%s.tar.gz" %(backup_dir,i))
        except:
            pass
    make_tarfile("%s\\minecraft-hour0.tar.gz"%backup_dir, minecraft_dir+"/")
    server_command("save-on")
    server_command("say Backup complete. World now saving. ")
    try:
        t = Timer(next_backuptime(), backup) # FIND NEXT HOURLY MARK
        t.start() # START BACKUP FOR THEN
    except:
        logging.info('',exc_info=True)

def next_backuptime():
    x=datetime.today()
    y=x.replace(hour=x.hour+1, minute=0, second=0, microsecond=0)
    delta_t=y-x
    secs=delta_t.seconds+1
    return secs

try:
    process=server_start() # START SERVER
    time.sleep(60) # WAIT FOR IT TO START
except:
    logging.info('',exc_info=True)

try:
    t = Timer(next_backuptime(), backup) # FIND NEXT HOURLY MARK
    t.start() # START BACKUP FOR THEN
except:
    logging.info('',exc_info=True)
