from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'


urlpatterns = [
path('registration/',views.registration, name='registration' ),
path('login/', auth_views.LoginView.as_view(), name='login'),
path('logout/', auth_views.LogoutView.as_view(), name='logout'),
path('profile/', views.profile, name='profile'),
path('menu/', views.menu, name='menu'),
path('order_submitted/', views.order_submitted, name='order_success'),
path('my-orders/', views.user_order, name='user_order'),
path('tables/', views.tables, name='tables'),
path('reservations/', views.reservations, name='reservations'),
path('cancel-reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
]