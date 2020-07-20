from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('menu/', views.menu, name='menu'),
    path('search/', views.search, name='search'),
    path('download/<int:id>', views.download_file, name='download'),
    path('accounts/sign_up/',views.SignUpView.as_view(), name="signup")
]