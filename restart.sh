# pkill -f "uvicorn backend-2dbs:app"
# sleep 2
# uvicorn backend-2dbs:app --host 0.0.0.0 --port 31337 --app-dir /root/rarbg-dump

cd /root/rarbg-dump

tmux kill-ses -t uvicorn
sleep 3

tmux new -s uvicorn -d
tmux send-keys 'TZ='Europe/Moscow' uvicorn backend-2dbs:app --host 0.0.0.0 --port 31337 --log-config uvicorn_logging.conf' C-m