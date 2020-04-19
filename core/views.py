from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView,View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import hashlib
import binascii
import random
from random import randint
from django.http import JsonResponse,HttpResponseRedirect,HttpResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from PayTm import Checksum
from django.shortcuts import redirect
from django.db import models
from django.template import loader
from django.forms import modelformset_factory
from .models import CarDetails,BookingDetails,Profile,Cart
from django.contrib.auth.models import User
# Create your views here.
from .forms import ProfileForm,RideForm
from django.utils import timezone
from datetime import datetime
import pytz
from django.template.defaulttags import register
from django.contrib import auth


utc=pytz.UTC

MERCHANT_KEY = 'S2lNTT66jYR5eMii';



def HomeView(request):
    if request.method == 'POST':
     
        s_date_str = request.POST['start_date'] 
        e_date_str = request.POST['end_date'] 
        #s_date = b[6:10] + '-' + b[0:2]+ '-' + b[3:5] 
        #e_date = e[6:10] + '-' + e[0:2]+ '-' + e[3:5] 
        
        s_date = datetime.strptime(s_date_str,"%m/%d/%Y %H:%M")
        e_date = datetime.strptime(e_date_str,"%m/%d/%Y %H:%M")

        #print("######################################################")
        #print("######################################################")
        #print("date pickerrrrrrrrrrr : ", s_date, type(s_date))
        #print("date pickerrrrrrrrrrr : ", e_date, type(e_date))
        #print("######################################################")
        #print("date pickerrrrrrrrrrr : ", s_date_str, type(s_date_str))
        #print("date pickerrrrrrrrrrr : ", e_date_str, type(e_date_str))
        #print("######################################################")
        #print("######################################################")

        request.session['b_date'] = str(s_date)
        request.session['be_date'] = str(e_date)

        b_cars = BookingDetails.objects.filter( is_ride_completed = False)
        #for car in booked_cars:
        #    print(car.Car_reg_no)
        #booked cars reg numbers list
        b_cars_reg_no = []
        for car in b_cars:
            if not iscaravailable(s_date, e_date , car.Ride_start_date.replace(tzinfo=utc), car.Ride_end_date.replace(tzinfo=utc) ):
                b_cars_reg_no.append(car.Car_reg_no)


        #b_cars_reg_no = list(str(car.Car_reg_no ) for car in b_cars)
        #print(len(b_cars_reg_no))
        availablecars = CarDetails.objects.exclude(Car_reg_no__in = b_cars_reg_no ).order_by( 'Make_model' , 'No_of_rides' )
        available_models=[]
        
        #TODO : nO : OOF BOOKINGS
        #eliminating cars of same models so as to avoid redundant display of cars
        for car in availablecars:
            if car.Make_model in available_models:
                b_cars_reg_no.append(car.Car_reg_no)                        
            else:
                available_models.append(car.Make_model)

        availablecars_final = CarDetails.objects.exclude(Car_reg_no__in = b_cars_reg_no ).order_by( 'Make_model')
        

        #print(len(b_cars_reg_no) , len(availablecars) , len(availablecars_final)    )
        
        return render(request, 'available.html', {'cars': availablecars_final , 's_date' : str(s_date) , 'e_date' : str(e_date)})

    else:
        # TODO : reducing view redundancy
        user_form = RideForm()
        return render(request, 'index.html', {'cars': CarDetails.objects.all().order_by( 'Make_model' ).distinct('Make_model') , 'my_form': user_form})

def iscaravailable(startdate,enddate,b_startdate,b_enddate ):
    startdate   = pytz.utc.localize(startdate)
    enddate   = pytz.utc.localize(enddate)
    b_startdate = timezone.template_localtime(b_startdate)
    b_enddate   = timezone.template_localtime(b_enddate)
    #print("#################################################################################################")
    #print(startdate ,type(startdate))
    #print(enddate  , type(enddate))
    #print(b_startdate)
    #print(b_enddate)
    #print("#################################################################################################")

    if startdate < b_startdate and enddate < b_startdate or startdate > b_enddate and enddate > b_enddate:
        return True
    else:
        return False



def logincolorlib(request):
    return render(request, 'logincolorlib.html')


#def AvailableView(request):
    #excludedcars = list(str(car.Car_reg_no) for car in BookingDetails.objects.all())
    #print(excludedcars)
    #print(len(excludedcars))
    #availablecars = CarDetails.objects.exclude(Car_reg_no__in = excludedcars)
    #print(availablecars)
    #print(len(availablecars))
    #return render(request, 'available.html', {'cars': availablecars })
#class AvailableView(ListView):
#    model = CarDetails
#    template_name = 'available.html'

def profile(request):
    user_object = User.objects.filter(username = request.user.username )
    user_form   = user_object[0]
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            #username       = form.cleaned_data['Username']
            #License        = form.cleaned_data['License_Number']
            #Mobile         = form.cleaned_data['Mobile_Number']
            #birthdate      = form.cleaned_data['BirthDate']
            #return render(request, 'profile.html')
            #print(username,License,Mobile,birthdate)
            user_object = User.objects.filter(username = request.user.username )
            user_form = user_object[0]
            user_form.profile.License = form.cleaned_data['License_Number']
            user_form.profile.Mobile = form.cleaned_data['Mobile_Number']
            user_form.profile.birthdate = form.cleaned_data['BirthDate']
            user_form.profile.Profile_status = "PENDING"
            user_form.save()
            # TODO : profile page view on submitting data
            return render(request, 'profile.html')
        else :
            return render(request, 'profile.html')
    else:
        context ={'user' : user_form } 
        initial_dict = { } 
        initial_dict["Username"] = request.user.username
        context['form']= ProfileForm(initial = initial_dict)
        return render(request, 'profile.html',context)
        #TODO : based on status what template shouls display


def iscaravalilable_final(b_date2,be_date2,Car_reg_no):
    bookings_object = BookingDetails.objects.filter(Car_reg_no = Car_reg_no, is_ride_completed = False)
    for car in bookings_object:
        if iscaravalilable(b_date2,be_date2,car.Ride_start_date,car.Ride_end_date) == False:
            return False
    return True


def Calculate_total_price (start,end,Price):
    diff = end - start
    Total = diff.days * Price
    hours = diff.seconds // 3600
    Total+= hours * 100
    return Total

@login_required
def CarDetailView(request, slug):
    car = get_object_or_404(CarDetails, pk=slug)
    #BOOKING_DICT['car'] = car.Car_reg_no
    #print(BOOKING_DICT)
    b_date2_str  = request.session.get('b_date') 
    be_date2_str = request.session.get('be_date')
    b_date2      = datetime.strptime(b_date2_str,"%Y-%m-%d %H:%M:%S")
    be_date2     = datetime.strptime(be_date2_str,"%Y-%m-%d %H:%M:%S")
    
    #print("------------------------------------------------------")
    #print("######################################################")
    #print("date pickerrrrrrrrrrr : ", b_date2, type(b_date2))
    #print("date pickerrrrrrrrrrr : ", be_date2, type(be_date2))
    #print("######################################################")
    #print("date pickerrrrrrrrrrr : ", b_date2_str, type(b_date2_str))
    #print("date pickerrrrrrrrrrr : ", be_date2_str, type(be_date2_str))
    #print("######################################################")
    #print("------------------------------------------------------")
    

    Total_price = Calculate_total_price (b_date2,be_date2,car.Price)
    #b_date2      = pytz.utc.localize(b_date2)
    #be_date2      = pytz.utc.localize(be_date2)
    #print("hhhhhhhhhhhhhhhhhmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")
    #print("date pickerrrrrrrrrrr : ", b_date2, type(b_date2))
    #print("date pickerrrrrrrrrrr : ", be_date2, type(be_date2))
    #print(" hhhhhhhhhhhhhhhhhmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm ")
    #print("------------------------------------------------------")
    #TODO : check whether this is required
    if request.user.is_authenticated and request.user.profile.Profile_status != "VERIFIED":
        #print(request.user.profile.No_of_bookings)
        return redirect('/profile/')

    if request.method=="POST":
        #TODO : once again check whether car is available
        if iscaravalilable_final(b_date2,be_date2,car.Car_reg_no):
            user_id = User.objects.get(username = request.user.username)
            random_number = str(random.randrange(2000000000, 9999999999, 2))
            unique_booking_id_2 = str(car.Car_reg_no) + '_' + str(user_id.profile.License) + '_' + random_number
        # TODO : License Number in cart
       
            cart_objects = Cart.objects.all()
            cart_users_list = list(str(cart_object.User_id) for cart_object in cart_objects )
            
            #checking if any bookings of the user in cart
            if request.user.username in cart_users_list:
                
                existing_user_obj = Cart.objects.filter( User_id = user_id.pk )
                #checking if more than one instance of a particular user exsts in cart
                existing_user_obj.delete()
                # TODO : Booked_for_kms to be added below
                # TODO : check Payment_start_time 
                Cart.objects.create(Car_reg_no = CarDetails.objects.get(Car_reg_no = car.Car_reg_no ) , User_id = User.objects.get(username = request.user.username), License = user_id.profile.License , Ride_start_date = b_date2 , Ride_end_date = be_date2 , unique_booking_id = unique_booking_id_2  )

            # if there is no instance of a user in cart
            else:
                Cart.objects.create(Car_reg_no = CarDetails.objects.get(Car_reg_no = car.Car_reg_no ) , User_id = User.objects.get(username = request.user.username), License = user_id.profile.License , Ride_start_date = b_date2 , Ride_end_date = be_date2, unique_booking_id = unique_booking_id_2  )
        
        #hash_object = hashlib.sha256(b'randint(0,20)')
        #txnid=hash_object.hexdigest()[0:20]
            param_dict = {
            'MID':'PZEISE83277279104814',
            'ORDER_ID': unique_booking_id_2,
            'TXN_AMOUNT': str(Total_price),
            'CUST_ID':'lordganesha',
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'WEBSTAGING',
            'CHANNEL_ID':'WEB',
	        'CALLBACK_URL':'https://selfdrive2.herokuapp.com/handlerequest/',
                }
            param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)

            return render(request, 'paytm.html',{'param_dict': param_dict  })
        else:
            #TODO : pass a message saying car booked by others please try again.......
            return render(request, 'index.html')
    return render(request, 'book.html',{'car': car , 'b_date2' : str(b_date2) , 'be_date2' : str(be_date2) ,  'Total_price' : Total_price , 'Days' : (be_date2 - b_date2).days , 'Hours': ((be_date2 - b_date2).seconds) // 3600  })


@csrf_exempt
def handlerequest(request):
    #auth.login(request, user)
    #print("USSSSSSSSSSERRRRRRRRRRRRRRRRRRRRRR", request.user.username)
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            #print('order successful')
            #Cart.objects.create(Car_reg_no = CarDetails.objects.get(Car_reg_no = car.Car_reg_no ) , User_id = User.objects.get(username = request.user.username),  Ride_date = b_date2 , unique_booking_id = unique_booking_id_2  )
            order_id = response_dict['ORDERID']
            
            cart_instance = Cart.objects.get(unique_booking_id = order_id)
            car_instance = CarDetails.objects.get(Car_reg_no = cart_instance.Car_reg_no)
            Total_price_cal = Calculate_total_price (cart_instance.Ride_start_date,cart_instance.Ride_end_date,car_instance.Price)
            # TODO : Extra fare and Price in BookingDetails
            Booking_instance = BookingDetails.objects.create(unique_booking_id = cart_instance.unique_booking_id, Car_reg_no = cart_instance.Car_reg_no , Make_model = car_instance.Make_model ,User_id = cart_instance.User_id, License = cart_instance.License, Ride_start_date = cart_instance.Ride_start_date, Ride_end_date = cart_instance.Ride_end_date ,  Price = car_instance.Price, Total_price = Total_price_cal,Transaction_id = str(response_dict['TXNID']) , Bank_txn_id = str(response_dict['BANKTXNID']) , Transaction_date =  str(response_dict['TXNDATE']) )
            Booking_instance.save()
            return render(request, 'paymentstatus.html', {'response': response_dict , 'bd': Booking_instance , 'car' : car_instance})
           
        else:
            #print('order was not successful because' + response_dict['RESPMSG'])
    
            return render(request, 'paymentstatus.html', {'response': response_dict })









@login_required
def BookingsView(request):
    user_id = User.objects.get(username = request.user.username)
    b_past    = BookingDetails.objects.filter(User_id = user_id.pk , is_ride_completed = True )
    b_ongoing = BookingDetails.objects.filter(User_id = user_id.pk , is_ride_ongoing   = True )
    b_new     = BookingDetails.objects.filter(User_id = user_id.pk , is_ride_completed = False )
    b_all     = BookingDetails.objects.filter(User_id = user_id.pk )
    c_all     =  CarDetails.objects.distinct('Make_model')
    images_links = {}
    for c in c_all:
        images_links[c.Make_model] = c.Image_url
    #print(images_links)
    #print("LLLLLLLLLLEEEEEE",len(images_links))
    return render(request, 'mybookings.html' , {'b_past' : b_past, 'b_ongoing' : b_ongoing, 'b_new' : b_new , 'images' : images_links})


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)