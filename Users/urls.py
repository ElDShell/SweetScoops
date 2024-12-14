from django.urls import path
from .views import *
urlpatterns = [
     # User authentication (login,logout,register...etc)
     path('login/',Login.as_view(),name='login'),
     path('logout/', LogoutView.as_view(), name='logout'),
     path("register/", UserCreateView.as_view(), name="register"),
     ## User profile
     path('profile/<slug:slug>/',ProfileDetailView.as_view(),name='profile_detail'),
     path('profile/<slug:slug>/image/update', ProfileImageUpdateView.as_view(), name='profile_image_update'),
     path('profile/<slug:slug>/phone/update', ProfilePhoneUpdateView.as_view(), name='profile_phone_update'),
     
     ## User 
     path('update/<str:signed_url>/fullname', UserFullNameUpdateView.as_view(), name='user_update_fullname'),
     path('update/<str:signed_url>/email', UserEmailUpdateView.as_view(), name='user_update_email'),
     path('update/<str:signed_url>/address', UserAddressUpdateView.as_view(), name='user_update_address'),

]
