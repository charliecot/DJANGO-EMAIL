from django.urls import path,include
from .views import UserRegistration,activate,index


urlpatterns = [
    path('', index , name='index'),
    path('account/register/', UserRegistration ,name='register' ),
    path('activate/<str:uidb64>/<str:token>/',activate, name='activate'),
    path('account/',include('django.contrib.auth.urls')),
]
