# Generated by Django 4.2.14 on 2024-08-12 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_usersdetails_referral_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersdetails',
            name='referral_code',
            field=models.CharField(default='Pebx9Uc3N29LMBT,', max_length=30),
        ),
    ]
