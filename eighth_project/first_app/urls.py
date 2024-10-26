from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('pass_change/', views.pass_change, name='passchange'),
    path('profile/', views.profile, name='profile'),
    path('first_app/', views.CarListView.as_view(), name='car_list'),
    path('first_app/<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),
    
    
]