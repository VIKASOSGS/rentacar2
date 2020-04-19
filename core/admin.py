from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile
# Register your models here.
from .models import CarDetails,BookingDetails,Cart
# Register your models here.

class BookingDetailsAdmin(admin.ModelAdmin):
    list_display = ('unique_booking_id','Make_model', 'Price','Total_price', 'Final_price'   , 'is_ride_completed')


class CarDetailsAdmin(admin.ModelAdmin):
    list_display = ('Car_reg_no', 'Make_model', 'Price' , 'Sitting_capacity', 'Fareperkm', 'Make_year' ,'Kms_driven' )


class CartAdmin(admin.ModelAdmin):
    list_display = ('unique_booking_id', 'User_id' , 'Car_reg_no' ,'Payment_start_time')


admin.site.register(CarDetails,CarDetailsAdmin)
admin.site.register(BookingDetails,BookingDetailsAdmin)
admin.site.register(Cart,CartAdmin)



class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)