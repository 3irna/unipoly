# Generated by Django 4.2.14 on 2024-08-21 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_alter_improvetask_social_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='improvetask',
            name='social_name',
            field=models.CharField(choices=[('Twitter', 'Twitter'), ('YouTube', 'YouTube'), ('Instagram', 'Instagram'), ('Telegram', 'Telegram')], max_length=20),
        ),
    ]
