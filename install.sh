pip3 install virtualenv
python3 -m virtualenv virtm
source virtm/bin/activate
pip3 install -r requirements.txt
./manage.py makemigrations
./manage.py makemigrations executor
./manage.py migrate