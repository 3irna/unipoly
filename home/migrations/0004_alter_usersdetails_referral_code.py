# Generated by Django 4.2.14 on 2024-08-12 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_usersdetails_is_add_mobile_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersdetails',
            name='referral_code',
            field=models.CharField(default='vrlqv3iD6eVtanJP', max_length=30),
        ),
    ]
