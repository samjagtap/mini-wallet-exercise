from django.contrib.auth.models import User
from exercise.wallets.models import Customer


def run():
    print("Initializing the mini-wallet-exercise app by creating necessary things.")
    if not User.objects.filter(username='test').first():
        user = User.objects.create(username='test', email='example@test.com')
        customer = Customer.objects.create(customer_profile=user)
        customer_xid = customer.customer_xid
        print("Setup complete. Your customer_xid is {}".format(customer_xid))
    else:
        user = User.objects.filter(username='test').first()
        customer = Customer.objects.filter(customer_profile=user).first()
        customer_xid = customer.customer_xid
        print("Setup complete. Your customer_xid is {}".format(customer_xid))
