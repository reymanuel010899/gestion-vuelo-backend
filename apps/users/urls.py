from django.urls import path
from . import views
app_name = 'users'


urlpatterns = [
    path('api/login/', views.LoginView.as_view(), name='login'),
    path('api/create-user/', views.Crearusuarioview.as_view()),
    path('api/logout/', views.logoutView.as_view(), name='logout')
]