mkdir -p /root/.vntrader /root/.vntrader/log
gunicorn --bind 0.0.0.0:8000 --workers 4 appmd:appmd