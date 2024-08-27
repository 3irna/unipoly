from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from home.views import home_page, UserRegister, GetUserInfo, UpdateUserCoin, UpdatePhone, home_page_reload, \
    CreateTaskForUsers, GetAllTasks, ResetUsersCoinPool, ConfirmTaskCode
from plinko import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

    path('admin/unp/', admin.site.urls),
    path('', home_page_reload),
    path('<init_data>', home_page),

    # api
    path('account/register', UserRegister.as_view()),
    path('account/get-userInfo', GetUserInfo.as_view()),
    path('account/update-userCoin', UpdateUserCoin.as_view()),
    path('account/update-mobile', UpdatePhone.as_view()),
    path('account/get-all-improve-task', GetAllTasks.as_view()),
    path('account/create-task-for-users', CreateTaskForUsers.as_view()),
    path('account/reset-users-pool', ResetUsersCoinPool.as_view()),
    path('account/send-and-confirm-code', ConfirmTaskCode.as_view()),

]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
