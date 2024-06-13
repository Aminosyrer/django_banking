from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from banking.models.costumer_rank import Customer_rank
from banking.models.account_type import Account_type
from banking.models.customer import Customer
from decimal import Decimal

class Command(BaseCommand):
    def handle(self, **options):
        admin, created = User.objects.get_or_create(username='admin')
        if created:
            admin.is_staff = True
            admin.is_superuser = True
            admin.password = make_password('123456')
            admin.save()

        employee_group, created = Group.objects.get_or_create(name='Employee')

        employee, created = User.objects.get_or_create(username='employee')
        if created:
            employee.is_staff = True
            employee.password = make_password('123456')
            employee.save()
            employee.groups.add(employee_group)

        if not Customer_rank.objects.all():
            blue_rank = Customer_rank.objects.create(name='Blue')
            silver_rank = Customer_rank.objects.create(name='Silver')
            gold_rank = Customer_rank.objects.create(name='Gold')
        else:
            blue_rank = Customer_rank.objects.get(name='Blue')
            silver_rank = Customer_rank.objects.get(name='Silver')
            gold_rank = Customer_rank.objects.get(name='Gold')

        if not Account_type.objects.all():
            Account_type.objects.create(name='Regular', interest_rate=Decimal(2.10))
            Account_type.objects.create(name='Savings', interest_rate=Decimal(5.75))
            Account_type.objects.create(name='Loan', interest_rate=Decimal(12.32))

        users_data = [
            {'username': 'blueuser', 'password': '123456', 'first_name': 'Blue', 'last_name': 'User', 'email': 'blueuser@example.com', 'rank': blue_rank},
            {'username': 'silveruser', 'password': '123456', 'first_name': 'Silver', 'last_name': 'User', 'email': 'silveruser@example.com', 'rank': silver_rank},
            {'username': 'golduser', 'password': '123456', 'first_name': 'Gold', 'last_name': 'User', 'email': 'golduser@example.com', 'rank': gold_rank}
        ]

        for user_data in users_data:
            user, created = User.objects.get_or_create(username=user_data['username'])
            if created:
                user.first_name = user_data['first_name']
                user.last_name = user_data['last_name']
                user.email = user_data['email']
                user.password = make_password(user_data['password'])
                user.save()

                Customer.objects.get_or_create(
                    user=user,
                    customer_rank=user_data['rank'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    email=user_data['email'],
                    phone='1234567890'
                )
