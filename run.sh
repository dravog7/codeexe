source virtm/bin/activate
sudo rabbitmq-server -detached
trap 'kill %1;kill %2;' SIGINT
celery -A codeexe worker -l info & ./manage.py runserver
trap - SIGINT