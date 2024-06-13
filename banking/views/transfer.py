from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from banking.forms.transfer import TransferForm
from banking.models.account import Account
from banking.models.ledger import Transaction, Ledger
from decimal import Decimal

@login_required
def transfer(request, customer_pk):
    customer = get_object_or_404(Customer, pk=customer_pk)
    
    if request.method == 'POST':
        form = TransferForm(request.POST, customer=customer)
        if form.is_valid():
            from_account = form.cleaned_data['from_account']
            to_account = form.cleaned_data['to_account']
            amount = form.cleaned_data['amount']
            
            if from_account.balance < amount:
                return HttpResponse('Insufficient funds')

            try:
                with transaction.atomic():
                    tnx = Transaction.objects.create()

                    # Debit from_account
                    Ledger.objects.create(
                        transaction=tnx,
                        customer=customer,
                        account=from_account,
                        amount=-amount
                    )

                    # Credit to_account
                    Ledger.objects.create(
                        transaction=tnx,
                        customer=to_account.customer,
                        account=to_account,
                        amount=amount
                    )

                    return redirect('banking:customer/accounts', customer_pk=customer.pk)

            except Exception as e:
                return HttpResponse('Error occurred: {}'.format(e))
    else:
        form = TransferForm(customer=customer)

    context = {'form': form, 'customer': customer}
    return render(request, 'banking/transfer.html', context)