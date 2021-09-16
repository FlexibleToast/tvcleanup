import os
import time
import sys
import logging
import pycron

########################################################################

path = os.environ['TV_PATH']
showList = os.environ['CONF']
logfile = os.environ['LOG']
exclude = os.environ['EXCLUDE'].split(',')
cron = os.environ['CRON']
uid = int(os.environ['PUID'])
gid = int(os.environ['PGID'])

############################# End Variables ############################


def main():
  logging.info("************Begin TV Cleanup************")
  inFile = open(showList)
  for line in inFile:
    line = line.rstrip('\n')
    token = line.split(",")
    cleanup(int(token[0]), os.path.join(path, token[1]))
  inFile.close()
  logging.info("*************End TV Cleanup*************")

#-----------------------------------------------------------------------
def clean(cleanPath, cleanItem):
  if os.path.isdir(cleanPath):
    try:
      os.rmdir(cleanPath)
      logging.info("Removed directory: " + cleanPath)
    except OSError:
      logging.error("Unable to remove directory: " + cleanPath)
  else:
    if not cleanPath.endswith(tuple(exclude)):
      try:
        if os.path.exists(cleanPath):
          os.remove(cleanPath)
          logging.info("Removed show: " + cleanItem)
      except OSError:
        logging.error("Unable to remove show: " + cleanItem)
#-----------------------------------------------------------------------
def cleanup(numDays, cleanPath):
  numSecs = time.time() - (numDays * 24 * 60 * 60)
  for root, dirs, files in os.walk(cleanPath):
    for name in files:
      filename = os.path.join(root, name)
      
      if os.stat(filename).st_mtime < numSecs:
        clean(filename, name)
      if not os.listdir(root):
        clean(root, name)
#-----------------------------------------------------------------------


os.chdir(path)
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
logging.info("Starting TVcleanup with cron " + cron)

os.setgid(gid)
os.setuid(uid)

logging.info("Using user ID: " + str(os.getuid()) + ", and group ID: " + str(os.getgid()))

while True:
  if pycron.is_now(cron):
    main()
    time.sleep(60)
  else:
    time.sleep(60)
