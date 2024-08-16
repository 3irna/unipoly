from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, Permission
from django.contrib.auth.models import User
import random


def create_referral_code():
    char_and_num = 'abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    code = random.choices(char_and_num, k=16)
    referral_code = ''.join(code)
    return referral_code


class UsersDetails(models.Model):
    for_user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=20)
    mobile = models.CharField(max_length=60, null=True, blank=True)
    total_referrals = models.IntegerField(default=0)
    referral_code = models.CharField(max_length=30)
    level = models.IntegerField(default=1, null=True, blank=True)
    level_xp = models.IntegerField(default=0, null=True, blank=True)
    unp_token = models.FloatField(default=0)
    coin_count = models.FloatField(default=0, null=True, blank=True)
    coin_pool = models.IntegerField(default=2000)
    can_take_from_pool = models.IntegerField(default=2000)
    coin_per_tap = models.IntegerField(default=1)
    is_add_mobile = models.BooleanField(default=False)
    last_update = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.for_user.username


class UserReferrals(models.Model):
    for_user = models.ForeignKey(User, on_delete=models.CASCADE)
    my_referral = models.ForeignKey(UsersDetails, on_delete=models.CASCADE)

    def __str__(self):
        return self.for_user.username


socials_ = {
    ("YouTube", "YouTube"),
    ("Instagram", "Instagram"),
    ("Telegram", "Telegram"),
    ("Twitter", "Twitter"),
}


class ImproveTask(models.Model):
    social_name = models.CharField(max_length=20, choices=socials_)
    task_name = models.CharField(max_length=100)
    task_code = models.CharField(max_length=100)
    prize_coin = models.IntegerField()
    date = models.DateTimeField()
    is_active = models.BooleanField()
    task_link = models.TextField()

    def __str__(self):
        return self.social_name



