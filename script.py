from django.contrib.auth.models import User
from exercise.wallets.models import Customer


def run_script():
    if not User.objects.filter(username='test').first():
        user = User.objects.create(username='test', email='example@test.com')
        customer = Customer.objects.create(customer_profile=user)
        customer_xid = customer.customer_xid
        print("Your customer_xid is {}".format(customer_xid))
    else:
        user = User.objects.filter(username='test').first()
        customer = Customer.objects.filter(customer_profile=user).first()
        customer_xid = customer.customer_xid
        print("Your customer_xid is {}".format(customer_xid))


run_script()
