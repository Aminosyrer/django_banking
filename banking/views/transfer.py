from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse
from banking.forms.transfer import TransferForm
from banking.models.account import Account
from banking.models.ledger import Ledger, Transaction
from banking.models.customer import Customer
from banking.models.ledger import generate_balance

@login_required
def transfer(request, customer_pk):
    customer = get_object_or_404(Customer, pk=customer_pk)

    if request.method == 'POST':
        form = TransferForm(request.POST, customer=customer)
        if form.is_valid():
            from_account = form.cleaned_data['from_account']
            to_account = form.cleaned_data['to_account']
            amount = form.cleaned_data['amount']

            from_account = generate_balance([from_account])[0]

            if from_account.balance < amount:
                return HttpResponse('Insufficient funds', status=400)

            with transaction.atomic():
                tnx = Transaction()
                tnx.save()

                Ledger.objects.create(
                    transaction=tnx,
                    customer=customer,
                    account=from_account,
                    amount=-amount
                )
                Ledger.objects.create(
                    transaction=tnx,
                    customer=to_account.customer,
                    account=to_account,
                    amount=amount
                )

            return redirect(reverse('banking:customer/accounts', args=[customer.pk]))
    else:
        form = TransferForm(customer=customer)

    return render(request, 'banking/customer/transfer.html', {'form': form, 'customer': customer})