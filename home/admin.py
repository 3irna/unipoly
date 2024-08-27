from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from home.models import UsersDetails, UserReferrals, ImproveTask, UserWantDoTask, FillDailyPoolTime


class UserWantDoTaskAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'for_task', 'is_complete']

    class Meta:
        model = UserWantDoTask


class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'mobile', 'unp_token', 'coin_count', 'total_referrals']
    search_fields = ["for_user__username"]
    ordering = ['coin_count']

    class Meta:
        model = UsersDetails


class UserReferralsAdmin(admin.ModelAdmin):
    class Meta:
        model = UserReferrals


class ImproveTaskAdmins(admin.ModelAdmin):
    list_display = ['__str__', 'task_code', 'date', 'is_active']

    class Meta:
        model = ImproveTask


admin.site.register(UsersDetails, UserDetailsAdmin)
#admin.site.register(UserReferrals, UserReferralsAdmin)
admin.site.register(ImproveTask, ImproveTaskAdmins)
admin.site.register(UserWantDoTask, UserWantDoTaskAdmin)
admin.site.register(FillDailyPoolTime)
