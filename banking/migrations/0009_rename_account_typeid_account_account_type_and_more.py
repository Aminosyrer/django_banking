# Generated by Django 4.2.5 on 2023-10-14 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('banking', '0008_alter_transaction_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='account_typeid',
            new_name='account_type',
        ),
        migrations.RenameField(
            model_name='account',
            old_name='customerid',
            new_name='customer',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='user_id',
            new_name='user',
        ),
    ]