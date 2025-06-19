from django.urls import path
from accounts.views import RegisterView
from django.contrib.auth import views as auth_views
from .views import activate_account

app_name = 'accounts'
urlpatterns = [
    
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate'),
]
