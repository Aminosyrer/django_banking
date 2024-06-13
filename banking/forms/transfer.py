from django import forms
from banking.models.account import Account
from django.db.models import Q

class TransferForm(forms.Form):
    from_account = forms.ModelChoiceField(queryset=Account.objects.all(), label='From Account')
    to_account = forms.ModelChoiceField(queryset=Account.objects.all(), label='To Account')
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label='Amount')

    def __init__(self, *args, **kwargs):
        customer = kwargs.pop('customer', None)
        super(TransferForm, self).__init__(*args, **kwargs)
        if customer:
            self.fields['from_account'].queryset = Account.objects.filter(customer=customer)
            self.fields['to_account'].queryset = Account.objects.filter(~Q(customer=customer))
