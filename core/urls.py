from django.urls import path
from .views import HomeView,CarDetailView,handlerequest,profile,logincolorlib,BookingsView
#AvailableView,
app_name = 'core'
urlpatterns = [
    path('', HomeView, name='homepage'),
    #path('available/', AvailableView, name='available'),
    #path('book/<slug>/', CarDetailView.as_view(), name='book'),
    path('book/<slug>/', CarDetailView, name='book'),
    path('handlerequest/', handlerequest, name='HandleRequest'),
    path('profile/', profile, name='profile'),
    path('logincolorlib/', logincolorlib, name='logincolorlib'),
    path('mybookings/', BookingsView, name='bookings'),

]


