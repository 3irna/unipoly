from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from home.models import UsersDetails, UserReferrals, ImproveTask


class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'unp_token', 'coin_count', 'total_referrals']

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
admin.site.register(UserReferrals, UserReferralsAdmin)
admin.site.register(ImproveTask, ImproveTaskAdmins)
