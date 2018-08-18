sudo apt-get install rabbitmq-server
sudo apt install firejail
sudo rabbitmqctl add_user user1 hey
sudo rabbitmqctl add_vhost host
sudo rabbitmqctl set_permissions -p host user1 ".*" ".*" ".*"
pip3 install virtualenv
python3 -m virtualenv virtm
source virtm/bin/activate
pip3 install -r requirements.txt
./manage.py makemigrations
./manage.py makemigrations executor
./manage.py migrate
./manage.py createsuperuser