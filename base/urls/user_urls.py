from django.urls import path
from base.views import user_views as views

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    path('register/' , views.registerUser , name='register'),
    
    path('profile/' ,views.getUserProfil, name="users-profile"),   
    path('profile/update/' ,views.updateUserProfil, name="users-profile-update"),   
    path('' ,views.getUsers, name="users"),   

    path('update/<str:pk>/' ,views.updateUser, name="user"),   
    path('<str:pk>/' ,views.getUserById, name="user-delete"),   
    path('delete/<str:pk>/' ,views.deleteUser, name="user-delete"),   

  ]