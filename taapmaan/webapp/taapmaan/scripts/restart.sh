#!/bin/sh

#START = "python /home/taapmaan/webapp/taapmaan/scripts/restart.sh &"
RESTART="nohup /home/taapmaan/webapp/taapmaan/scripts/script.sh >> /tmp/script.out 2>&1 &"

PGREP="/usr/bin/pgrep"

SCRIPT="runner.py"

$PGREP -f ${SCRIPT}

if [ $? -ne 0 ] 
then
  $RESTART
else
  kill -9 `$PGREP -f ${SCRIPT}`
  sleep 1
  $RESTART
fi
