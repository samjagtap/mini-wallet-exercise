import uuid
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User
from djchoices.choices import DjangoChoices, ChoiceItem
from rest_framework.authtoken.models import Token


class Customer(TimeStampedModel):
    customer_xid = models.UUIDField(max_length=255, default=uuid.uuid4, primary_key=True)
    customer_profile = models.OneToOneField(User, related_name='customer', on_delete=models.deletion.PROTECT)

    def regenerate_user_token(self):
        try:
            # Delete old token if exists.
            token = Token.objects.get(user=self.customer_profile)
            token.delete()
        except Exception:
            pass

        # Create fresh/new token.
        token = Token.objects.create(user=self.customer_profile)
        return token


class Wallet(TimeStampedModel):
    class Statuses(DjangoChoices):
        Enabled = ChoiceItem('enabled', 'Enabled')
        Disabled = ChoiceItem('disabled', 'Disabled')

    id = models.UUIDField(max_length=255, default=uuid.uuid4, primary_key=True)
    owned_by = models.OneToOneField(Customer, related_name='wallet', on_delete=models.deletion.PROTECT)
    status = models.CharField(max_length=50, choices=Statuses.choices, default=Statuses.Disabled, null=False, blank=False)
    enabled_at = models.DateTimeField(null=True, blank=True)
    disabled_at = models.DateTimeField(null=True, blank=True)
    balance = models.DecimalField(max_digits=15, decimal_places=4, default=0, null=True, blank=True)


class Transaction(TimeStampedModel):
    class TransactionTypes(DjangoChoices):
        Deposit = ChoiceItem('deposit', 'Deposit')
        Withdrawal = ChoiceItem('withdrawal', 'Withdrawal')

    class TransactionStatuses(DjangoChoices):
        Success = ChoiceItem('success', 'Success')
        Failed = ChoiceItem('failed', 'Failed')

    id = models.UUIDField(max_length=255, default=uuid.uuid4, primary_key=True)
    transaction_by = models.ForeignKey(Customer, related_name='transactions', on_delete=models.deletion.PROTECT)
    transaction_type = models.CharField(max_length=50, choices=TransactionTypes.choices, null=False, blank=False)
    status = models.CharField(max_length=50, choices=TransactionStatuses.choices, null=False, blank=False)
    transaction_at = models.DateTimeField(null=True, blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
    reference_id = models.UUIDField(max_length=255, default=uuid.uuid4)
    wallet = models.ForeignKey(Wallet, related_name='transactions', on_delete=models.deletion.PROTECT)

    def update_wallet_balance(self):
        if self.transaction_type == Transaction.TransactionTypes.Deposit:
            self.wallet.balance += int(self.amount)
            self.wallet.save()
            return "Success"

        elif self.transaction_type == Transaction.TransactionTypes.Withdrawal:
            if self.wallet.balance >= int(self.amount):
                self.wallet.balance -= int(self.amount)
                self.save()
                return "Success"
            else:
                return "Failed"
