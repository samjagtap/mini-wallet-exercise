import datetime
from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Customer, Wallet, Transaction


class GetTokenView(GenericAPIView):
    """This view is not protected by Token Authentication.
     So that customer can get his/her token by providing customer_xid."""

    def post(self, request, *args, **kwargs):
        customer_xid = request.data.get('customer_xid', None)
        if customer_xid and len(customer_xid) == 36:
            print(len(customer_xid))
            customer = Customer.objects.filter(customer_xid=str(customer_xid)).first()
            if customer:
                # Create wallet/account for customer if not exists.
                wallet = Wallet.objects.filter(owned_by=customer).first()
                if not wallet:
                    Wallet.objects.create(owned_by=customer)
                # Generate token for customer.
                token = customer.regenerate_user_token()
                response = {"data": {"token": token.key},
                            "status": "success"}
            else:
                response = {"detail": "Customer not exists with given customer_xid"}
        else:
            response = {"detail": "Invalid customer_xid"}
        return Response(response)


class WalletView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.filter(customer_profile=request.user).first()
        wallet = Wallet.objects.filter(owned_by=customer).first()
        if wallet and wallet.status == Wallet.Statuses.Enabled:
            response = {"status": "success",
                        "data": {
                            "wallet": {
                                "id": wallet.id,
                                "owned_by": wallet.owned_by.customer_xid,
                                "status": wallet.status,
                                "enabled_at": wallet.enabled_at,
                                "balance": wallet.balance
                            }
                        }
                        }
        else:
            response = {"detail": "Your wallet is disabled. Please enable it first in order to see your wallet balance."}
        return Response(response)

    def post(self, request, *args, **kwargs):
        customer = Customer.objects.filter(customer_profile=request.user).first()
        wallet = Wallet.objects.filter(owned_by=customer).first()
        if wallet and wallet.status == Wallet.Statuses.Disabled:
            wallet.status = Wallet.Statuses.Enabled
            wallet.enabled_at = datetime.datetime.now()
            wallet.save()
            response = {"status": "success",
                        "data": {
                            "wallet": {
                                "id": wallet.id,
                                "owned_by": wallet.owned_by.customer_xid,
                                "status": wallet.status,
                                "enabled_at": wallet.enabled_at,
                                "balance": wallet.balance
                            }
                        }
                        }
        else:
            response = {'detail': "Your wallet is already enabled."}
        return Response(response)

    def patch(self, request, *args, **kwargs):
        is_disabled = request.data.get('is_disabled', None)
        customer = Customer.objects.filter(customer_profile=request.user).first()
        wallet = Wallet.objects.filter(owned_by=customer).first()
        if wallet and wallet.status == Wallet.Statuses.Enabled:
            if is_disabled == 'true':
                wallet.status = Wallet.Statuses.Disabled
                wallet.disabled_at = datetime.datetime.now()
                wallet.save()
                response = {"status": "success",
                            "data": {
                                "wallet": {
                                    "id": wallet.id,
                                    "owned_by": wallet.owned_by.customer_xid,
                                    "status": wallet.status,
                                    "disabled_at": wallet.disabled_at,
                                    "balance": wallet.balance
                                }
                            }
                            }
            else:
                response = {"detail": "Value of is_disabled must be true."}
        else:
            response = {'detail': "Your wallet is already disabled."}
        return Response(response)


class DepositView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        amount = request.data.get('amount', None)
        reference_id = request.data.get('reference_id', None)
        if amount and reference_id and len(reference_id) == 36:
            if not Transaction.objects.filter(reference_id=reference_id).first():
                customer = Customer.objects.filter(customer_profile=request.user).first()
                wallet = Wallet.objects.filter(owned_by=customer).first()
                if wallet and wallet.status == Wallet.Statuses.Enabled:
                    transaction = Transaction.objects.create(transaction_by=customer,
                                                             transaction_type=Transaction.TransactionTypes.Deposit,
                                                             status=Transaction.TransactionStatuses.Success,
                                                             transaction_at=datetime.datetime.now(),
                                                             amount=int(amount),
                                                             reference_id=reference_id,
                                                             wallet=wallet)
                    transaction.update_wallet_balance()
                    transaction.save()
                    response = {"status": "success",
                                "data": {
                                    "deposit": {
                                        "id": transaction.id,
                                        "deposited_by": transaction.transaction_by.customer_xid,
                                        "status": "success",
                                        "deposited_at": transaction.transaction_at,
                                        "amount": transaction.amount,
                                        "reference_id": transaction.reference_id
                                    }
                                }
                                }
                else:
                    response = {"detail": "Your wallet is disabled. Enable it first in order to make deposits."}
            else:
                response = {"detail": "One deposit already present with this reference_id. Please try with different reference_id."}
        else:
            response = {"detail": "Enter the amount and reference_id correctly."}
        return Response(response)


class WithdrawalView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        amount = request.data.get('amount', None)
        reference_id = request.data.get('reference_id', None)
        if amount and reference_id and len(reference_id) == 36:
            if not Transaction.objects.filter(reference_id=reference_id).first():
                customer = Customer.objects.filter(customer_profile=request.user).first()
                wallet = Wallet.objects.filter(owned_by=customer).first()
                if wallet and wallet.status == Wallet.Statuses.Enabled:
                    if int(amount) <= int(wallet.balance):
                        transaction = Transaction.objects.create(transaction_by=customer,
                                                                 transaction_type=Transaction.TransactionTypes.Withdrawal,
                                                                 status=Transaction.TransactionStatuses.Success,
                                                                 transaction_at=datetime.datetime.now(),
                                                                 amount=int(amount),
                                                                 reference_id=reference_id,
                                                                 wallet=wallet)
                        transaction.update_wallet_balance()
                        transaction.save()
                        response = {"status": "success",
                                    "data": {
                                        "withdrawal": {
                                            "id": transaction.id,
                                            "withdrawn_by": transaction.transaction_by.customer_xid,
                                            "status": transaction.status,
                                            "withdrawn_at": transaction.transaction_at,
                                            "amount": transaction.amount,
                                            "reference_id": transaction.reference_id
                                        }
                                    }
                                    }
                    else:
                        response = {"detail": "Insufficient funds in your wallet. Withdrawal could not be processed."}
                else:
                    response = {"detail": "Your wallet is disabled. Enable it first in order to make withdrawals."}
            else:
                response = {"detail": "One withdrawal already present with this reference_id. Please try with different reference_id."}
        else:
            response = {"detail": "Enter the amount and reference_id correctly."}
        return Response(response)
