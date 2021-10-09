# Mini Wallet Exercise
Mini Wallet Exercise

# System requirements
Python 3.6.7
Ubuntu 20.04

# Clone the code
git clone https://github.com/samjagtap/mini-wallet-exercise.git

# If you don't already have virtualenv then install .You can install them as follows.
sudo apt-get install python3-pip
sudo pip3 install virtualenv

# Then set up your virtual env
virtual .env
source .env/bin/activate
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Run setup script then run the django app

source .env/bin/activate 
python manage.py runscript setup_customer --traceback
python manage.py runserver_plus 

Then you can access your instance on the port and url specified. But it should be something like this https://127.0.0.1:8000
