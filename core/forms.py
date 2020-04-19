from allauth.account.forms import SignupForm 
from django import forms
from django.forms import ModelForm
from core.models import Profile
from datetime import datetime, timedelta
# File: forms.py
from bootstrap_datepicker_plus import DatePickerInput,DateTimePickerInput

class RideForm(forms.Form):
    start_date = forms.DateField(  widget=DateTimePickerInput(  
        options = {
           "collapse" : False,
            "minDate" : (datetime.now() + timedelta(hours = 2)).strftime("%m/%d/%Y %H:%M"),
            "stepping" : "30",
            "sideBySide" : True,
            

        },
        attrs={'style' : 'height: 50px;padding-top: 0px;padding-bottom: 0px;'  }
      ))

    end_date = forms.DateField( required = False , widget=DateTimePickerInput(  
        options = {
            "collapse" : False,
            "minDate" : ( datetime.now() + timedelta(days = 1, hours = 2)).strftime("%m/%d/%Y %H:%M"),
            "stepping" : "30",
            "sideBySide" : True,
        },
        attrs={'style' : 'height: 50px;padding-top: 0px;padding-bottom: 0px;'}
      ))
  

class CustomSignupForm(SignupForm): 
    first_name = forms.CharField(max_length=30, label='First Name') 
    last_name = forms.CharField(max_length=30, label='Last Name') 
    def signup(self, request, user): 
        user.first_name = self.cleaned_data['first_name'] 
        user.last_name = self.cleaned_data['last_name']
        user.save() 
        return user 


#class ProfileModelForm(ModelForm):
#    class Meta:
#        model = Profile
#        fields = "__all__"


# creating a form 
class ProfileForm(forms.Form): 
    Username       = forms.CharField(max_length = 200,widget=forms.TextInput(attrs={'readonly':'readonly',"class" : "form-control text-center" ,'style' : 'height: 50px;padding-top: 0px;padding-bottom: 0px; font-size : 22px'} ))
    BirthDate     = forms.DateField(  widget=DatePickerInput(  
        options = {
           "collapse" : False,
            "maxDate" : (datetime.now() - timedelta(hours = 157600)).strftime("%m/%d/%Y"),
            },
        attrs={'style' : 'height: 50px;padding-top: 0px;padding-bottom: 0px;'  }
      ))
    License_Number = forms.CharField(max_length = 200 , required = True, strip = True,widget=forms.TextInput(attrs={'placeholder': 'TS02720180000000' ,  "class" : "form-control" , 'style' : 'height: 50px;padding-top: 0px;padding-bottom: 0px; font-size : 18px'} )) 
    Mobile_Number  = forms.CharField(max_length = 10, required = True, strip = True,widget=forms.TextInput(attrs={'placeholder': '9999999999',"class" : "form-control" , 'style' : 'height: 50px;padding-top: 0px;padding-bottom: 0px; font-size : 18px'} ) ) 
   