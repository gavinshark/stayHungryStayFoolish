import threading
import datetime
from time import sleep

STR_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
#can only run in cmd but not debug
def loopfunc():
  strCurrentTime = datetime.datetime.utcnow().strftime(STR_DATETIME_FORMAT)
  sleep(1)
  print("Hello, World! at %s" % strCurrentTime)

def printit():  
  threading.Timer(2.0, printit).start()
  loopfunc()

printit()