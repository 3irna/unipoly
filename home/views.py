import time
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserResgisterSerializer, GetUserInfoSerializer, ValidateInitDataSerializer, \
    UpdatePhoneSerializer, UserWantDoTaskSerializer, GetAllTasksSerializer, ValidateResetPool, ConfirmTaskCodeSerializer
from .models import UsersDetails, UserReferrals, ImproveTask, create_referral_code, UserWantDoTask, FillDailyPoolTime
from home.validate_api import validate_init_data
from plinko.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_BOT_ID
from rest_framework import status
import requests
from django.utils import timezone
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit


class ResetUsersCoinPool(APIView):
    def get(self, request):
        ser_token = ValidateResetPool(data=request.POST)
        if ser_token.is_valid() and ser_token.validated_data['token'] == TELEGRAM_BOT_TOKEN:
            for user in UsersDetails.objects.all():
                user.can_take_from_pool = 2000
                user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class GetAllTasks(APIView):
    def post(self, request):
        ser_init_data = ValidateInitDataSerializer(data=request.POST)
        if ser_init_data.is_valid():
            is_valid, user_data = validate_init_data(str(ser_init_data.validated_data['init_data']))
            if is_valid:
                all_task = ImproveTask.objects.all()
                ser_all_task = GetAllTasksSerializer(instance=all_task, many=True)
                return Response(data=ser_all_task.data, status=status.HTTP_200_OK)
        return Response(ser_init_data.errors)


class ConfirmTaskCode(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='user', rate='5/h', method='POST'))
    def post(self, request):
        ser_data = ConfirmTaskCodeSerializer(data=request.POST)
        try:
            if ser_data.is_valid():
                is_valid, user_data = validate_init_data(str(ser_data.validated_data['init_data']))
                if is_valid:
                    my_task = ImproveTask.objects.get(id=ser_data.validated_data['task_id'])
                    my_user = UsersDetails.objects.get(user_id=user_data['id'])
                    if UserWantDoTask.objects.filter(for_task=my_task, for_user=my_user, is_need_code=True,
                                                     is_complete=False).exists():
                        want_this_task = UserWantDoTask.objects.get(for_task=my_task, for_user=my_user,
                                                                    is_need_code=True,
                                                                    is_complete=False)
                        ts_now = time.time()
                        if ts_now - want_this_task.start_time > 240:
                            pass
                        else:
                            return Response("please_do_task")
                        if want_this_task.code == ser_data.validated_data['task_code']:
                            pass
                        else:
                            return Response("code_is_invalid")

                        want_this_task.is_complete = True
                        want_this_task.save()

                        my_user.coin_count += my_task.prize_coin
                        my_user.level_xp += my_task.prize_coin
                        my_user.task_pool += my_task.prize_tap
                        my_user.save()
                        return Response("ok", status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateTaskForUsers(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='user', rate='10/h', method='POST'))
    def post(self, request):
        ser_data = UserWantDoTaskSerializer(data=request.POST)
        if ser_data.is_valid():
            is_valid, user_data = validate_init_data(str(ser_data.validated_data['init_data']))
            if is_valid:
                ts_now = time.time()
                try:
                    task = ImproveTask.objects.get(id=ser_data.validated_data['task_id'])
                    user = UsersDetails.objects.get(user_id=user_data['id'])
                except:
                    return Response("Task is not exist", status=status.HTTP_404_NOT_FOUND)

                if not UserWantDoTask.objects.filter(for_task=task, for_user=user).exists():
                    if task.social_name == 'Telegram':
                        task_created = UserWantDoTask.objects.create(for_task=task, for_user=user, start_time=ts_now,
                                                                     is_complete=False)
                    elif task.is_need_enter_code:
                        task_created = UserWantDoTask.objects.create(for_task=task, for_user=user, start_time=ts_now,
                                                                     is_complete=False, is_need_code=True,
                                                                     code=task.task_code)
                        return Response("200", status=status.HTTP_200_OK)
                    else:
                        task_created = UserWantDoTask.objects.create(for_task=task, for_user=user, start_time=ts_now,
                                                                     is_complete=True)
                        user.coin_count += task.prize_coin
                        user.level_xp += task.prize_coin
                        user.save()

                    return Response(ser_data.data['task_id'], status=status.HTTP_200_OK)
                return Response('this task has already been done', status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response("User not valid", status=status.HTTP_404_NOT_FOUND)
        return Response("Data not valid", status=status.HTTP_404_NOT_FOUND)


class UpdateUserCoin(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='user', rate='5000/d', method='POST'))
    def post(self, request):  # get coin and coin_can_take for update in database
        is_valid, user_data = validate_init_data(request.POST['init_data'])
        if is_valid:
            try:
                coin = request.POST['coin']
                pool_name = request.POST['pool_name']
            except:
                coin = 0

            user = UsersDetails.objects.get(user_id=user_data['id'])
            if float(coin) > user.can_take_from_pool + user.task_pool + 500:
                user.cheat_count += 1
                user.save()
                return Response(status=status.HTTP_204_NO_CONTENT)

            new_coin = int(user.coin_count) + int(coin)
            user.coin_count = new_coin
            user.level_xp = new_coin

            if pool_name == "main_pool":
                can_take_from_pool = user.can_take_from_pool - int(coin)
                if can_take_from_pool <= 0:
                    user.can_take_from_pool = 0
                else:
                    user.can_take_from_pool = can_take_from_pool

            elif pool_name == "task_pool":
                can_take_from_task_pool = user.task_pool - int(coin)
                if can_take_from_task_pool <= 0:
                    user.task_pool = 0
                else:
                    user.task_pool = can_take_from_task_pool

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

            return Response("this user is not coming from Telegram", status=status.HTTP_404_NOT_FOUND)

        return Response(ser_init_data.errors)


class UserRegister(APIView):  # this api only call in bot side when users start btn
    @method_decorator(ratelimit(key='user', rate='10000/h', method='POST'))
    def post(self, request):
        ser_data = UserResgisterSerializer(data=request.POST)
        if ser_data.is_valid() and not User.objects.filter(username=ser_data.validated_data['username']).exists() and \
                not UsersDetails.objects.filter(user_id=ser_data.validated_data['password']).exists():
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
            return Response(ser_data.data, status=status.HTTP_200_OK)

        if UsersDetails.objects.filter(user_id=request.POST['password']).exists():
            try:
                if UsersDetails.objects.get(user_id=request.POST['password']).is_add_mobile:
                    return Response("mobile_is_active", status=status.HTTP_201_CREATED)
                else:
                    return Response("mobile_is_not", status=status.HTTP_404_NOT_FOUND)
            except:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(ser_data.errors, status=status.HTTP_403_FORBIDDEN)


class UpdatePhone(APIView):
    @method_decorator(ratelimit(key='user', rate='2/d', method='POST'))
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
                    add_ref_for_my_referrer.level_xp += 1000
                    add_ref_for_my_referrer.save()

                user_update_mobile.save()

                return Response('Mobile Updated', status=status.HTTP_200_OK)
            return Response('token is incorrect', status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response("error", status=status.HTTP_403_FORBIDDEN)


def home_page_reload(request):
    context = {}
    return render(request, "home.html", context=context)


def is_member_of_channel(chat_id, user_id):  # ex : chat_id = @channel_username
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getChatMember"
        params = {
            "chat_id": chat_id,
            "user_id": user_id
        }
        resp = requests.get(url, data=params)
        return resp.json()['ok']
    except:
        return False


def home_page(request, init_data=None):
    try:
        is_valid, user_data = validate_init_data(init_data)
    except:
        is_valid = False
    if is_valid:
        username = user_data['username']
        password = user_data['id']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        all_users = UsersDetails.objects.all().order_by('coin_count').reverse()
        total_coin_earned = 0
        for user in all_users:
            total_coin_earned += user.level_xp

        user_info = UsersDetails.objects.get(user_id=user_data['id'])
        referral_link = f'https://t.me/{TELEGRAM_BOT_ID}?start={user_info.referral_code}'
        my_referrals = UserReferrals.objects.filter(for_user__username=user_info.for_user.username)

        if user_info.total_referrals >= 10 and not user_info.is_reach_10_ref:
            user_info.coin_count += 10000
            user_info.level_xp += 10000
            user_info.is_reach_10_ref = True
            user_info.save()
        if user_info.total_referrals >= 20 and not user_info.is_reach_20_ref:
            user_info.coin_count += 20000
            user_info.level_xp += 20000
            user_info.is_reach_20_ref = True
            user_info.save()
        if user_info.total_referrals >= 30 and not user_info.is_reach_30_ref:
            user_info.coin_count += 30000
            user_info.level_xp += 30000
            user_info.is_reach_30_ref = True
            user_info.save()

        all_simple_tasks = ImproveTask.objects.filter(is_need_enter_code=False).reverse()

        all_public_tack_need_code = ImproveTask.objects.filter(is_need_enter_code=True)
        all_task_need_code = ImproveTask.objects.filter(
            userwantdotask__for_user=user_info, userwantdotask__is_complete=False, is_need_enter_code=True)
        tasks_need_need_code = all_public_tack_need_code.union(all_task_need_code)
        user_task_complete = UserWantDoTask.objects.filter(for_user=user_info, is_complete=True).reverse()
        task_need_confirm_code = UserWantDoTask.objects.filter(for_user=user_info, is_complete=False)

        a = all_public_tack_need_code.difference(ImproveTask.objects.filter(
            userwantdotask__for_user=user_info, userwantdotask__is_complete=True))

        user_task_not_complete = UserWantDoTask.objects.filter(for_user=user_info, is_complete=False)
        for task in user_task_not_complete:
            if task.for_task.is_need_check_channel:
                is_joined = is_member_of_channel(task.for_task.channel_username, user_info.user_id)
                if is_joined:
                    user_info.coin_count += task.for_task.prize_coin
                    user_info.level_xp += task.for_task.prize_coin
                    user_info.save()
                else:
                    task.delete()

        task_completed_id = []
        for my_task in user_task_complete:
            task_completed_id.append(my_task.for_task.id)

        set_user_level = int(user_info.level_xp / 100000)
        user_info.level = set_user_level + 1
        user_info.save()

        time_now = timezone.now().time()
        fill_time = FillDailyPoolTime.objects.all().first().fill_time.time()

        hour = fill_time.hour - time_now.hour
        minute = fill_time.minute - time_now.minute
        second = fill_time.second - time_now.second

        fill_time_second = hour * 60 * 60 + minute * 60 + second
        if fill_time_second < 0:
            if hour <= 0:
                hour += 23
            if minute <= 0:
                minute += 59
            if second <= 0:
                second += 59
            fill_time_second = hour * 60 * 60 + minute * 60 + second

        context = {
            'total_coin_earned': total_coin_earned,
            'total_players': all_users.count(),
            'users': all_users,
            'referral_link': referral_link,
            'my_referrals': my_referrals,
            'my_user_info': user_info,
            'all_task': all_simple_tasks,
            'my_task': user_task_complete,
            'task_is_com': task_completed_id,
            'fill_time': fill_time_second,
            'tasks_need_code': all_public_tack_need_code,
            'task_need_confirm': task_need_confirm_code,
            'public_task_need_code': a,
        }
    else:
        context = {}
    return render(request, "home.html", context=context)
