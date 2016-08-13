bind = "0.0.0.0:8080"
worker_class = "eventlet"
w = 1
forwarded_allow_ips = "*"
accesslog = "/app/user/gunicorn.access.log"
errorlog = "/app/user/gunicorn.error.log"
