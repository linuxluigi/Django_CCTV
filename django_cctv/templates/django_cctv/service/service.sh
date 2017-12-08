#!/bin/sh
### BEGIN INIT INFO
# Provides:          {{ monitor }}
# Required-Start:    $local_fs $network $named $time $syslog
# Required-Stop:     $local_fs $network $named $time $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Description:       Capture video stream from ip-cam and send it to localhost rtmp server
### END INIT INFO

RUNAS={{ user }}

start() {
  if screen -list | grep -q '{{ monitor }}'; then
    echo 'Service already running' >&2
    return 1
  fi

  echo 'Starting service' >&2

  screen -dmS {{ monitor }} {{ path }}-run.sh

  echo 'Service started' >&2
}

stop() {
  if ! screen -list | grep -q '{{ monitor }}'; then
    echo 'Service not running' >&2
    return 1
  fi

  echo 'Stopping service' >&2
  screen -X -S {{ monitor }} quit
  echo 'Service stopped' >&2
}

uninstall() {
  echo -n "Are you really sure you want to uninstall this service? That cannot be undone. [yes|No] "
  local SURE
  read SURE
  if [ "$SURE" = "yes" ]; then
    force-uninstall
  fi
}

purge() {
  echo "This service will be uninstalled!"
  stop
  # update-rc.d -f {{ monitor }} remove
  rm -fv "$0"
  rm -f {{ path }}-run.sh
}

case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  uninstall)
    uninstall
    ;;
  purge)
    purge
    ;;
  retart)
    stop
    start
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|uninstall|purge}"
esac