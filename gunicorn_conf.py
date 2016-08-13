bind = "0.0.0.0:8080"
worker_class = "eventlet"
w = 1
forwarded_allow_ips = "*"
accesslog = "/code/gunicorn.access.log"
errorlog = "/code/gunicorn.error.log"
