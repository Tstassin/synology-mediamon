#!/bin/sh
# /usr/local/etc/rc.d/S99mediamon.sh

case "$1" in
  start|"")
    #start the monitoring daemon
    python3 /usr/local/mediamon/mediamon.py
    ;;
  restart|reload|force-reload)
    echo "Error: argument '$1' not supported" >&2
    exit 3
    ;;
  stop)
    kill `cat /var/run/mediamon.pid`
    ;;
  *)
    echo "Usage: S99mediamon.sh [start|stop]" >&2
    exit 3
    ;;
esac
