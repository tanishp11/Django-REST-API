
from django.urls import path
from masterapp.views import *


urlpatterns = [
    path('sign-up',User_Signup.as_view(),name='sign-up'),
    path('login',User_login.as_view(),name='login'),
    path('update-profile/',User_udate_detail.as_view(),name='update-profile'),
]
