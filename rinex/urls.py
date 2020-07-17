from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('menu/', views.menu, name='menu'),
    path('search/', views.search, name='search'),
    #path('detail/<id:rinex>', views.detailRinex, name='detail'),
    path('accounts/sign_up/',views.SignUpView.as_view(), name="signup")
]