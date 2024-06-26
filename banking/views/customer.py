from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Sum
from django.contrib.auth.decorators import login_required
from banking.forms.new_loan_application import LoanApplicationForm
from banking.forms.new_customer import CustomerForm
from banking.models.account import Account, LoanApplication
from banking.models.ledger import Ledger, generate_balance
from banking.models.account_type import Account_type
from banking.forms.new_account import AccountForm
from banking.models.customer import Customer

@login_required
def index(request):
    customer = get_object_or_404(Customer, user=request.user)
    return redirect('banking:customer/detail', pk=customer.pk)

@login_required
def detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'PATCH':
       form = CustomerForm(request.PATCH, instance=customer, exclude_password_rank=True)
       if form.is_valid():
          customer = form.save()       
    else:
       form = CustomerForm(instance=customer, exclude_password_rank=True)
    context = {'customer': customer, 'customer_form': form}
    return render(request, 'banking/customer/customer_detail.html', context)
    
@login_required
def account_list(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    accounts = generate_balance(Account.objects.filter(~Q(account_type__name='Loan'), customer=pk))
    context = {'customer': customer, 'accounts': accounts}
    return render(request, 'banking/customer/account_list.html', context)

@login_required
def account_details(request, customer_pk, account_pk):
    customer = get_object_or_404(Customer, pk=customer_pk)
    account = generate_balance([get_object_or_404(Account, pk=account_pk)])[0]

    if request.method == 'PATCH':
       form = AccountForm(request.PATCH, instance=account, exclude_type=True)
       if form.is_valid():
          account.name = form.cleaned_data['name']
          account.save()
    else:
       form = AccountForm(instance=account, exclude_type=True)
    
    context = {'customer': customer, 'account': account, 'form': form}
    return render(request, 'banking/customer/account_details.html', context)

@login_required
def loan_application_list(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    loan_applications = LoanApplication.objects.filter(customer=customer)

    if customer.customer_rank.name not in ['Gold', 'Silver']:
        return HttpResponse('Only gold and silver ranked customers can apply for loans.')

    if request.method == 'POST':
       loan_form = LoanApplicationForm(customer, request.POST)
       if loan_form.is_valid():
           loan_application = loan_form.save(commit=False)
           account_name = request.POST.get('account')
           account = Account.objects.get(name=account_name)
           loan_application.account = account
           loan_application.customer = customer
           loan_application.save()
    else:
       loan_form = LoanApplicationForm(customer)

    context = {'customer': customer, 'loan_form': loan_form, 'loan_applications': loan_applications}
    return render(request, 'banking/customer/loan_application_list.html', context)

@login_required
def loans_list(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    loans = generate_balance(Account.objects.filter(account_type__name='Loan', customer=pk))
    print("Loans = ", loans)
    context = { 'customer': customer, 'loans': loans }
    return render(request, 'banking/customer/loan_list.html', context)
   
