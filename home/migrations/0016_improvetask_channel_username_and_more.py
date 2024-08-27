# Generated by Django 4.2.14 on 2024-08-20 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_alter_improvetask_social_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='improvetask',
            name='channel_username',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='improvetask',
            name='is_need_check_channel',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='improvetask',
            name='social_name',
            field=models.CharField(choices=[('YouTube', 'YouTube'), ('Instagram', 'Instagram'), ('Twitter', 'Twitter'), ('Telegram', 'Telegram')], max_length=20),
        ),
    ]
