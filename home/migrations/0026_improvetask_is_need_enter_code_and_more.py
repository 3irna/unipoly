# Generated by Django 4.2.14 on 2024-08-24 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0025_filldailypooltime_delete_filldailypool_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='improvetask',
            name='is_need_enter_code',
            field=models.BooleanField(default=False, help_text='If you enable this please fill below field'),
        ),
        migrations.AlterField(
            model_name='improvetask',
            name='channel_username',
            field=models.CharField(blank=True, help_text='Like : @unipoly', max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='improvetask',
            name='is_need_check_channel',
            field=models.BooleanField(default=False, help_text='If enable this option you need to fill below field'),
        ),
        migrations.AlterField(
            model_name='improvetask',
            name='social_name',
            field=models.CharField(choices=[('Instagram', 'Instagram'), ('YouTube', 'YouTube'), ('Twitter', 'Twitter'), ('Telegram', 'Telegram')], max_length=20),
        ),
        migrations.AlterField(
            model_name='improvetask',
            name='task_code',
            field=models.CharField(help_text='Take prize with this code (Enable is_need_enter_code)', max_length=100),
        ),
    ]
