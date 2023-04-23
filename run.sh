#!/bin/bash

konsole --noclose -e "redis-server" &
konsole --noclose -e "celery -A JPWP worker --loglevel=info" &
konsole --noclose -e "celery -A JPWP beat -l INFO" &
konsole --noclose -e "python3 manage.py runserver" &
