# Mini Wallet Exercise
Mini Wallet Exercise

### System requirements
1. Python 3.6.7
2. Ubuntu 20.04

### Clone the code
git clone https://github.com/samjagtap/mini-wallet-exercise.git

### If you don't already have virtualenv then install .You can install them as follows.
1. sudo apt-get install python3-pip
2. sudo pip3 install virtualenv

### Then set up your virtual env
1. virtual .env
2. source .env/bin/activate
3. pip install -r requirements.txt

### Run migrations
1. python manage.py makemigrations
2. python manage.py migrate

### Run setup script then run the django app

1. source .env/bin/activate 
2. python manage.py runscript setup_customer --traceback
3. python manage.py runserver

Then you can access your instance on the port and url specified. But it should be something like this https://127.0.0.1:8000
