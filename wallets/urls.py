from django.urls import path
from .views import GetTokenView, WalletView, DepositView, WithdrawalView


urlpatterns = [
    # Get Token and create the wallet for customer
    path('init', GetTokenView.as_view(), name='init'),

    # Enable, disable and view wallet balance
    path('wallet', WalletView.as_view(), name='wallet'),

    # Deposit virtual money into wallet
    path('wallet/deposits', DepositView.as_view(), name='wallet_deposits'),

    # Withdraw/spend virtual money from wallet
    path('wallet/withdrawals', WithdrawalView.as_view(), name='wallet_withdrawals'),
]
