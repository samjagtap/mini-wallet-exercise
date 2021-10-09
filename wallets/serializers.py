from rest_framework import serializers
from .models import Customer, Wallet, Transaction


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('customer_xid', 'customer_profile', 'created', 'modified')


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('id', 'owned_by', 'status', 'enabled_at', 'disabled_at', 'balance', 'created', 'modified')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'transaction_by', 'transaction_type', 'status', 'transaction_at', 'amount', 'reference_id',
                  'wallet', 'created', 'modified')
