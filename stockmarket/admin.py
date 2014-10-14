from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from stockmarket.models import Investor, Startup, Bank

# Register your models here.

class InvestorInline(admin.StackedInline):
    model = Investor
    can_delete = False
    verbose_name_plural = 'investor'

class UserAdmin(UserAdmin):
    inlines = (InvestorInline, )
    list_display = ('first_name','last_name','email', 'username', 'is_staff')
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


#class EntrepreneurAdmin(admin.ModelAdmin):
#    list_display = ('name','email','cash','password','id')
#admin.site.register(Entrepreneur, EntrepreneurAdmin)

class StartupAdmin(admin.ModelAdmin):
    list_display = ('startupName','ceo','askingPrice', 'id')

admin.site.register(Startup, StartupAdmin)

class BankAdmin(admin.ModelAdmin):
    list_display = ('buyer','seller','price', 'shares', 'timeStamp', 'id')

admin.site.register(Bank, BankAdmin)
