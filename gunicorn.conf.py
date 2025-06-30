# gunicorn.conf.py

bind = "0.0.0.0:8000"
workers = 2  # número de procesos trabajadores
accesslog = "-"  # logs al stdout
errorlog = "-"
loglevel = "info"
timeout = 120

#1