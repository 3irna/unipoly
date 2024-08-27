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
    for_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="username")
    user_id = models.CharField(max_length=20)
    mobile = models.CharField(max_length=60, null=True, blank=True)
    is_add_mobile = models.BooleanField(default=False, verbose_name="mobile confirmed")
    total_referrals = models.IntegerField(default=0, verbose_name="number of referrals")
    referral_code = models.CharField(max_length=30)
    level = models.IntegerField(default=1, null=True, blank=True)
    level_xp = models.IntegerField(default=0, null=True, blank=True)
    unp_token = models.FloatField(default=0)
    coin_count = models.FloatField(default=0, null=True, blank=True, verbose_name="unp coin")
    coin_pool = models.IntegerField(default=2000, verbose_name="coin pool size")
    task_pool = models.IntegerField(default=0, verbose_name="task pool size")
    can_take_from_pool = models.IntegerField(default=2000, verbose_name="coin in the pool")
    coin_per_tap = models.IntegerField(default=1)
    last_update = models.IntegerField(null=True, blank=True, verbose_name="last coin updated")

    is_reach_10_ref = models.BooleanField(default=False, verbose_name="has 10 referrals")
    is_reach_20_ref = models.BooleanField(default=False, verbose_name="has 20 referrals")
    is_reach_30_ref = models.BooleanField(default=False, verbose_name="has 30 referrals")

    cheat_count = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.for_user.username}(LVL.{self.level})"


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
    task_title = models.CharField(max_length=100)
    task_name = models.TextField(verbose_name="task description")
    prize_coin = models.IntegerField()
    prize_tap = models.IntegerField(default=2000)
    date = models.DateTimeField()
    is_active = models.BooleanField()
    task_link = models.TextField()
    is_need_check_channel = models.BooleanField(default=False, help_text="If enable this option you need to fill "
                                                                         "below field")
    channel_username = models.CharField(max_length=120, null=True, blank=True, help_text="Like : @unipoly")
    is_need_enter_code = models.BooleanField(default=False, help_text="If you enable this please fill below field")
    task_code = models.CharField(max_length=100, null=True, blank=True,
                                 help_text="Take prize with this code (Enable is_need_enter_code)")
    time_left = models.DateTimeField(null=True, blank=True, help_text="Set time left (Enable is_need_enter_code)")

    def __str__(self):
        return f"{self.social_name}-{self.id}"


class UserWantDoTask(models.Model):
    for_task = models.ForeignKey(ImproveTask, on_delete=models.CASCADE)
    for_user = models.ForeignKey(UsersDetails, on_delete=models.CASCADE)
    start_time = models.IntegerField(null=True, blank=True)
    is_need_code = models.BooleanField(default=False)
    code = models.CharField(max_length=100, null=True, blank=True)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.for_user.for_user.username


class FillDailyPoolTime(models.Model):
    fill_time = models.DateTimeField()

    def __str__(self):
        return self.fill_time.time().__str__()
