from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'users'

urlpatterns =[
    path('registration/', views.registration, name='registration'),
    path('login/', auth_views.LoginView.as_view() ,name='login'),
    path('logout/', auth_views.LogoutView.as_view() ,name='logout'),
    path('profile/', views.profile ,name='profile'),
    path('event_list/', views.event_list, name='event_list'),
    path('<int:pk>/event_registration/', views.event_registration, name='event_registration'),
    path('my_events/',views.my_events, name='my_events'),
    path('<int:event_id>/cancel_registration/', views.cancel_registration,name='cancel_registration'),
]
