from django.urls import path
from . import views

urlpatterns = [
    # /countrie_and_cities/
    path('', views.IndexView.as_view(), name='index'),

    # /countrie_and_cities/register/
    path('register/', views.register, name='register'),

    # /countrie_and_cities/login_user/
    path('login_user/', views.login_user, name='login_user'),

    # /countrie_and_cities/logout_user/
    path('logout_user/', views.logout_user, name='logout_user'),

    # /countrie_and_cities/city/<pk>/add/
    path('city/<pk>/add', views.CityCreate.as_view(), name='city-add'),

    # /countrie_and_cities/city/<pk>/update/
    path('city/<pk>/update', views.CityUpdate.as_view(), name='city-update'),

    # /countrie_and_cities/city/<pk>/delete/
    path('city/<pk>/delete', views.CityDelete.as_view(), name='city-delete')


]