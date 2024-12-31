
from django.urls import path
from masterapp.views import *

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('sign-up',User_Signup.as_view(),name='sign-up'),
    path('login',User_login.as_view(),name='login'),
    path('update-profile/',User_udate_detail.as_view(),name='update-profile'),

    path('category/add',add_category.as_view(),name='add-category'),
    path('sub-category/add',add_sub_category.as_view(),name='add-sub-category'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)