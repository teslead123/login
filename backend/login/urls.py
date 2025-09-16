from django.urls import path
from . import views
urlpatterns = [
    path('',views.home_view,name='home'),
    path('register/',views.register_view,name='register'),
    path('login/', views.login_view,name='login'),
    path('api/user/', views.UserView.as_view(), name='user'),
    path('api/dashboard/',views. DashboardView.as_view(), name='dashboard'),
    # path('receive-ip/', receive_ip, name='receive_ip'),
    path('get_local_ip/',views.get_local_ip,name='get_local_ip')
]
