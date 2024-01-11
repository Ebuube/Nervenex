# Build Nervenex


# Variables
# =========

# Compiler
CC = gunicorn

# Compiler flags
GFLAGS = --worker-class gevent --bind '0.0.0.0:80'

# Pip
PIP = pip
PFLAGS = install -r

# Source
API_SRC = api/v1/app.py
WEB_SRC = web_dynamic/app.py
PIP_SRC = requirements.txt

# Name
API_NAME = api.v1.app:app


.PHONY: api \
	web_dynamic


api: $(API_SCR)
	# sudo apt-get --assume-yes update
	# sudo apt-get --assume-yes install python3.7 python3-pip
	$(PIP) $(PFLAGS) $(PIP_SRC)
	$(CC) $(CFLAGS) $(API_NAME) &
