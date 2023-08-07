from django.urls import path
from .views import DistrictList, MandalList, ACList, secretariatList, Submit

urlpatterns = [
    path('get_district/', DistrictList.as_view(), name = 'get_ac'),
    path('get_ac/', ACList.as_view(), name = 'get_ac'),
    path('get_mandal/', MandalList.as_view(), name= 'get_mandal'),
    path('get_ward/', secretariatList.as_view(), name ='get_Ward'),
    path('submit/', Submit.as_view(), name ='submit'),
]
