#!/bin/bash

APP_NAME="app.py"
LOG_FILE="app.log"

start() {
    echo "Starting $APP_NAME..."
    nohup python3 $APP_NAME > $LOG_FILE 2>&1 &
    echo "$APP_NAME started with PID $!"
}

stop() {
    echo "Stopping $APP_NAME..."
    # 查找并杀死进程
    pkill -f $APP_NAME
    echo "$APP_NAME stopped."
}

restart() {
    stop
    start
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac