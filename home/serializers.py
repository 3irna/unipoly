from rest_framework import serializers
from home.models import UsersDetails, ImproveTask


class ValidateInitDataSerializer(serializers.Serializer):
    init_data = serializers.CharField(required=True)


class GetUserInfoSerializer(serializers.Serializer):
    for_user = serializers.CharField()
    total_referrals = serializers.IntegerField()
    level = serializers.IntegerField()
    level_xp = serializers.IntegerField()
    coin_count = serializers.FloatField()
    coin_pool = serializers.IntegerField()
    can_take_from_pool = serializers.IntegerField()
    coin_per_tap = serializers.IntegerField()


class UserResgisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    mobile = serializers.CharField(required=False)
    my_referrer = serializers.CharField(required=False)


class UpdatePhoneSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True)
    mobile = serializers.CharField(required=True)
    bot_token = serializers.CharField(required=False)


class UserWantDoTaskSerializer(serializers.Serializer):
    init_data = serializers.CharField(required=True)
    task_id = serializers.CharField(required=True)


class GetAllTasksSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    social_name = serializers.CharField()
    task_name = serializers.CharField()
    task_code = serializers.CharField()
    prize_coin = serializers.IntegerField()
    date = serializers.DateTimeField()
    is_active = serializers.BooleanField()
    task_link = serializers.CharField()


class ValidateResetPool(serializers.Serializer):
    token = serializers.CharField(required=True)


class ConfirmTaskCodeSerializer(serializers.Serializer):
    init_data = serializers.CharField(required=True)
    task_id = serializers.CharField(required=True)
    task_code = serializers.CharField(required=True)