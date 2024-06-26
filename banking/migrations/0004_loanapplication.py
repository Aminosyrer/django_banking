# Generated by Django 4.2.5 on 2023-10-01 21:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('banking', '0003_alter_account_type_interest_rate_ledger'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='banking.account')),
                ('customerid', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='banking.customer')),
            ],
        ),
    ]
