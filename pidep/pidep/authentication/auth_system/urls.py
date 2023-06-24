from django.urls import path
from .views import HomePage, Register, Login, test, logoutuser,profile

urlpatterns = [
    path('home/', HomePage, name="home-page"),
    path('register/', Register, name="register-page"),
    path('', Login, name="login-page"),
    path('logout/', logoutuser, name='logout'),
    path('test/', test, name='test'),
    path('profile/', profile, name='profile')

]