pkill redis-server; konsole --hold -e "redis-server" &
konsole --hold -e "celery -A JPWP worker --loglevel=info" &
konsole --hold -e "celery -A JPWP beat -l INFO" &
konsole --hold -e "python3 manage.py runserver"
