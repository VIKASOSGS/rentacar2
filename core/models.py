from django.db import models
from phone_field import PhoneField
from django.db.models import CharField, Value as V
from django.db.models.functions import Concat
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
# TODO : km package to be added
# TODO : may be unlimited 
class CarDetails(models.Model):
    TRANSMISSION     = [('AUTOMATIC' , 'Automatic'),('MANUAL' , 'Manual'),]
    FUEL             = [('PETROL' , 'Petrol'),('DIESEL' , 'Diesel'),]
    SITTING_CAPACITY = [('5','5')  ,  ('7'  ,  '7')]
    COLOR            = [('WHITE','White')  , ('GREEN','Green')  , ('RED', 'Red') ,('BLUE','Blue')]

    Car_reg_no       = models.CharField(max_length = 50, primary_key = True)
    Make_model       = models.CharField(max_length = 50)
    Make_year        = models.IntegerField()
    Transmission     = models.CharField(max_length = 9, choices = TRANSMISSION)
    Fuel             = models.CharField(max_length = 6, choices = FUEL)
    Kms_driven       = models.IntegerField(blank = True)
    Price            = models.IntegerField()
    Sitting_capacity = models.CharField(max_length = 1, choices = SITTING_CAPACITY)
    Fareperkm        = models.IntegerField(blank = True)
    color            = models.CharField(max_length = 8, choices = COLOR)
    Image_url        = models.URLField(blank = True)
    No_of_rides      = models.IntegerField( default = 0)
    Fareperhour      = models.IntegerField(default = 100)

    def __str__(self):
        return self.Car_reg_no

    def get_absolute_url(self):
        return reverse("core:book", kwargs={  "slug": self.Car_reg_no})

class Profile(models.Model):
    PROFILE_STATUS     = [('UNVERIFIED' , 'UNVERIFIED'),('PENDING' , 'PENDING'), ('VERIFIED' , 'VERIFIED')]
    user         = models.OneToOneField(User, on_delete=models.CASCADE)
    License      = models.CharField( max_length = 20,  null=True, blank = True)
    Mobile       = models.CharField(max_length = 10, null=True, blank=True, unique = True)
    birthdate    = models.DateField(null=True, blank=True)
    No_of_bookings = models.IntegerField(default = 0)
    Profile_status = models.CharField(max_length = 10, choices = PROFILE_STATUS , default = "UNVERIFIED")

    def __str__(self):  # __unicode__ for Python 2
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
    

class BookingDetails(models.Model):
    Car_reg_no        = models.ForeignKey(CarDetails, on_delete = models.DO_NOTHING)
    Make_model        = models.CharField( max_length = 50, blank = True)
    unique_booking_id = models.CharField(max_length=100 ,blank = True, null =True , unique = True)
    User_id           = models.ForeignKey(User,on_delete = models.DO_NOTHING,blank = True, null = True)
    License           = models.CharField( max_length = 20, blank = True)
    Kms_initial       = models.IntegerField(blank = True, null = True)
    Kms_later         = models.IntegerField(blank = True, null = True)
    Kms_Driven        = models.IntegerField(blank = True, null = True)
    Booked_for_kms    = models.IntegerField(blank = True, null = True)
    #TODO : caluculate total price
    Price             = models.IntegerField(blank = True,null = True)
    Total_price       = models.IntegerField(blank = True,null = True)
    Extra_fare        = models.IntegerField(blank = True,null = True)
    Booking_date      = models.DateTimeField(auto_now_add = True, blank = True,null = True)
    Ride_start_date   = models.DateTimeField(blank = True,null = True)
    Ride_end_date     = models.DateTimeField(blank = True,null = True)
    Ride_started_at   = models.DateTimeField(blank = True,null = True)
    Ride_ended_at     = models.DateTimeField(blank = True,null = True)
    Final_price       = models.IntegerField(blank = True,null = True)
    is_ride_completed = models.BooleanField(default = False)
    is_ride_ongoing   = models.BooleanField(default = False)
    Transaction_id    = models.CharField( max_length = 60, blank = True)
    Bank_txn_id       = models.CharField( max_length = 60, blank = True)
    Transaction_date  = models.CharField( max_length = 60, blank = True)
    #TODO : is_ride started


    def __str__(self):
        return self.unique_booking_id


class Cart(models.Model):
    Car_reg_no        = models.ForeignKey(CarDetails, on_delete = models.CASCADE)
    User_id           = models.ForeignKey(User,on_delete = models.CASCADE)
    License           = models.CharField( max_length = 20, blank = True, null = True)
    Booked_for_kms    = models.IntegerField(blank = True, null = True)
    Ride_start_date   = models.DateTimeField(blank = True,null = True)
    Ride_end_date     = models.DateTimeField(blank = True,null = True)
    Payment_start_time = models.DateTimeField(auto_now_add = True)
    unique_booking_id = models.CharField(max_length=100 ,blank = True, null =True)

    def __str__(self):
        return self.unique_booking_id

    
 



    #Booking_id=BookingDetails.objects.annotate(unique_booking_id=Concat('Car_reg_no', V('_'), 'License', V('_'),'id', output_field=CharField() )).get()
    
    #is_ride_ongoing   = 
    #Booking_date_from = models.
    #Booking_date_from = models.

    #class Meta:
    #    models.UniqueConstraint(fields= ['id','Car_reg_no','License'], name='unique_booking_id')


    #class UserDetails(models.Model):
#    License      = models.CharField(primary_key = True, max_length = 20)
#    Email        = models.EmailField(max_length=50)
#    Mobile       = models.CharField(max_length = 10, unique = True)
#    First_name   = models.CharField(max_length=50)
#    Last_name    = models.CharField(max_length=50)
#    License_image= models.ImageField(blank = True, upload_to=None, height_field=None, width_field=None, max_length=None)
#
#    def __str__(self):
#        return self.License
