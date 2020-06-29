from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('accounts/sign_up/',views.SignUpView.as_view(), name="signup")
]