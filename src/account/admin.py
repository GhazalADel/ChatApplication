from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account

class AccountAdmin(UserAdmin):
    list_display=('phone','username','date_joined','last_login','is_admin','is_staff')
    search_fields=('phone','username')
    readonly_fields=('id','last_login','date_joined')
    filter_horizontal=()
    list_filter=()
    fieldsets=()

admin.site.register(Account,AccountAdmin)