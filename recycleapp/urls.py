from django.urls import path
from .views import registerView, loginView, DashboardView, logoutApp, userProfile, RecycleView


app_name = 'recycleapp'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('register-user/', registerView, name='register'),
    path('login/', loginView, name='login'),
    path('logout/', logoutApp, name='logout'),
    path('profile/<int:pk>/', userProfile, name='profile'),
    path('card-board/', RecycleView.as_view(), name='card-board'),
]
