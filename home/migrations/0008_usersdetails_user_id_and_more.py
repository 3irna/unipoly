# Generated by Django 4.2.14 on 2024-08-13 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_alter_usersdetails_referral_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersdetails',
            name='user_id',
            field=models.CharField(default=23423, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usersdetails',
            name='referral_code',
            field=models.CharField(default='1vD9mc9N4P1wvlVn', max_length=30),
        ),
    ]
