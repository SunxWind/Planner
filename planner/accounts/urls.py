from django.urls import path
from .views import LoginView, register, AccountInfoView, logout_view, DashboardView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', register, name='register'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('account/', AccountInfoView.as_view(), name='account_info'),
    path('logout/', logout_view, name='logout'),
]
