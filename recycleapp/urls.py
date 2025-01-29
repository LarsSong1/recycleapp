from django.urls import path
from .views import registerView, loginView, DashboardView, logoutApp, userProfile, RecycleView, deleteRecyclingData, editRecyclingData, RecycleCenterView, claimMaterial 


app_name = 'recycleapp'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('register-user/', registerView, name='register'),
    path('login/', loginView, name='login'),
    path('logout/', logoutApp, name='logout'),
    path('profile/<int:pk>/', userProfile, name='profile'),
    path('recycle-view/', RecycleView.as_view(), name='recycle-view'),
    path('delete-recycling-data/<int:pk>/', deleteRecyclingData, name='delete-recycling-data'),
    path('edit-recycling-data/<int:pk>/', editRecyclingData, name='edit-recycling-data'),
    path('recycle-center/', RecycleCenterView.as_view(), name="recycle-center"),
    path("claim/<int:center_id>/", claimMaterial, name="claim_material"),

]
