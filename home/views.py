import time
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserResgisterSerializer, GetUserInfoSerializer, ValidateInitDataSerializer, \
    UpdatePhoneSerializer
from .models import UsersDetails, UserReferrals, ImproveTask, create_referral_code
from home.validate_api import validate_init_data
from plinko.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_BOT_ID


class UpdateUserCoin(APIView):
    def post(self, request):  # get coin and coin_can_take for update in database
        is_valid, user_data = validate_init_data(request.POST['init_data'])
        if is_valid:
            coin = request.POST['coin']
            coin_can_take = request.POST['coin_can_take']
            username = user_data['username']
            user = UsersDetails.objects.get(for_user__username=username)
            new_coin = int(user.coin_count) + int(coin)
            user.coin_count = new_coin
            user.can_take_from_pool = coin_can_take
            user.last_update = time.time()
            user.save()
            return Response("Update is completed")


class GetUserInfo(APIView):
    def post(self, request):
        ser_init_data = ValidateInitDataSerializer(data=request.POST)
        if ser_init_data.is_valid():  # check serializers validation
            is_valid, user_data = validate_init_data(str(ser_init_data.validated_data['init_data']))
            if is_valid:  # check validation from mini app Telegram for init app

                user_info = UsersDetails.objects.get(user_id=user_data['id'])

                ser_user_info = GetUserInfoSerializer(instance=user_info)

                return Response(data=ser_user_info.data)

            return Response("this user is not coming from Telegram")

        return Response(ser_init_data.errors)


class UserRegister(APIView):  # this api only call in bot side when users start btn
    def post(self, request):
        ser_data = UserResgisterSerializer(data=request.POST)
        if ser_data.is_valid() and not User.objects.filter(username=ser_data.validated_data['username']).exists():
            username = ser_data.validated_data['username']
            password = ser_data.validated_data['password']
            UsersDetails.objects.create(for_user=User.objects.create_user(
                username=username,
                password=password,
            ), user_id=password, referral_code=create_referral_code())

            my_referrer = ser_data.validated_data['my_referrer']
            if UsersDetails.objects.filter(referral_code=my_referrer).exists():
                my_referrer_username = UsersDetails.objects.get(referral_code=my_referrer)
                UserReferrals.objects.create(
                    for_user=User.objects.get(username=my_referrer_username),
                    my_referral=UsersDetails.objects.get(for_user__username=username)
                )
            return Response(ser_data.data)

        if UsersDetails.objects.filter(user_id=request.POST['password']).exists():
            if UsersDetails.objects.get(user_id=request.POST['password']).is_add_mobile:
                return Response("mobile_is_active")
            else:
                return Response("mobile_is_not")

        return Response(ser_data.errors)


class UpdatePhone(APIView):
    def post(self, request):
        ser_data = UpdatePhoneSerializer(data=request.POST)
        if ser_data.is_valid():
            if ser_data.validated_data['bot_token'] == TELEGRAM_BOT_TOKEN:
                user_update_mobile = UsersDetails.objects.get(user_id=ser_data.validated_data['user_id'])
                user_update_mobile.mobile = ser_data.validated_data['mobile']
                user_update_mobile.is_add_mobile = True

                if UserReferrals.objects.filter(my_referral=user_update_mobile).exists():
                    my_referrer = UserReferrals.objects.get(my_referral=user_update_mobile)
                    add_ref_for_my_referrer = UsersDetails.objects.get(for_user__username=my_referrer.for_user.username)
                    add_ref_for_my_referrer.total_referrals += 1
                    add_ref_for_my_referrer.coin_count += 1000
                    add_ref_for_my_referrer.save()

                user_update_mobile.save()

                return Response('Mobile Updated')
            return Response('token is incorrect')
        else:
            return Response("error")


def home_page_reload(request):
    context = {}
    return render(request, "home.html", context=context)


def home_page(request, init_data=None):
    try:
        is_valid, user_data = validate_init_data(init_data)
    except:
        is_valid = False
    if is_valid:

        all_users = UsersDetails.objects.all()
        total_coin_earned = 0
        for user in all_users:
            total_coin_earned += user.coin_count

        user_info = UsersDetails.objects.get(user_id=user_data['id'])
        referral_link = f'https://t.me/{TELEGRAM_BOT_ID}?start={user_info.referral_code}'
        my_referrals = UserReferrals.objects.filter(for_user__username=user_info.for_user.username)

        all_tasks = ImproveTask.objects.all()

        context = {
            'total_coin_earned': total_coin_earned,
            'total_players': all_users.count(),
            'users': all_users,
            'referral_link': referral_link,
            'my_referrals': my_referrals,
            'my_user_info': user_info,
            'all_task': all_tasks,
        }
    else:
        context = {}
    return render(request, "home.html", context=context)
