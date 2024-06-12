from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from banking.models.costumer_rank import Customer_rank  # Corrected import
from banking.models.account_type import Account_type
from decimal import Decimal

class Command(BaseCommand):
    def handle(self, **options):
        # Create admin if not exists and give staff and superuser permissions
        admin, created = User.objects.get_or_create(username='admin')
        if created:
            admin.is_staff = True
            admin.is_superuser = True
            admin.password = make_password('123456')
            admin.save()

        # Create supervisor if not exists and give staff permissions
        supervisor, created = User.objects.get_or_create(username='supervisor')
        if created:
            supervisor.is_staff = True
            supervisor.password = make_password('123456')
            supervisor.save()

        # Create Employee group if not exists
        employee_group, created = Group.objects.get_or_create(name='Employee')

        # Add supervisor to Employee group
        supervisor.groups.add(employee_group)

        # Create a sample employee user and add to Employee group
        employee, created = User.objects.get_or_create(username='employee')
        if created:
            employee.is_staff = True
            employee.password = make_password('123456')
            employee.save()
            employee.groups.add(employee_group)

        # Create customers ranks if table is empty
        if not Customer_rank.objects.all():
            Customer_rank.objects.create(name='Blue')
            Customer_rank.objects.create(name='Silver')
            Customer_rank.objects.create(name='Gold')

        # Create account types if table is empty
        if not Account_type.objects.all():
            Account_type.objects.create(name='Regular', interest_rate=Decimal(2.10))
            Account_type.objects.create(name='Savings', interest_rate=Decimal(5.75))
            Account_type.objects.create(name='Loan', interest_rate=Decimal(12.32))