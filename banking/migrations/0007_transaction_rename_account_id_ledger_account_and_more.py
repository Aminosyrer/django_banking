# Generated by Django 4.2.5 on 2023-10-14 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('banking', '0006_alter_loanapplication_customerid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.RenameField(
            model_name='ledger',
            old_name='account_id',
            new_name='account',
        ),
        migrations.RenameField(
            model_name='ledger',
            old_name='customer_id',
            new_name='customer',
        ),
        migrations.AddField(
            model_name='ledger',
            name='transaction',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='banking.transaction'),
            preserve_default=False,
        ),
    ]
