"""Gunicorn configuration file for ulga project."""

import multiprocessing

# Bind to Unix socket
bind = "unix:/var/run/ulga/gunicorn.sock"

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50

# Timeouts
timeout = 30
keepalive = 2

# Logging
accesslog = "/var/log/ulga/gunicorn-access.log"
errorlog = "/var/log/ulga/gunicorn-error.log"
loglevel = "info"

# Process naming
proc_name = "ulga"

# Server mechanics
daemon = False
pidfile = "/var/run/ulga/gunicorn.pid"
umask = 0o007
user = None  # Will be set by systemd
group = None  # Will be set by systemd

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190
