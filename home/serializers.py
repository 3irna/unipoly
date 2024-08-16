from rest_framework import serializers
from home.models import UsersDetails


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


