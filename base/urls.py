from django.urls import path
from . import views
from .views import donation_view, donation_success, edit_donation, recent_donations, indexx_view, contact_view, about_view
from .views import subscribe
from .views import donation_list



urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('room/<int:pk>/', views.room, name="room"),
    path('profile/<int:pk>/', views.userProfile, name="user-profile"),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<int:pk>/', views.updateRoom, name="update-room"),
    path('deleteRoom/<int:pk>/', views.deleteRoom, name="deleteRoom"),
    path('delete-message/<int:pk>/', views.deleteMessage, name="delete-message"),

    path('update-user/', views.updateUser, name="update-user"),

    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),

    path('donations/', donation_view, name='donation_page'),
    path('success/', donation_success, name='donation_success'),
    path('edit/<int:donation_id>/', edit_donation, name='edit_donation'),
    path('recent_donations/', views.recent_donations, name='recent_donations'),
    path('recent_donations/', views.recent_donations, name='recent_donations'),
    path('thank_you/', views.thank_you, name='thank_you'),
     path('donations/', donation_list, name='donation_list'),

    path('indexx/', indexx_view, name='indexx'),
    path('contact/', contact_view, name='contact'),
    path('about/', about_view, name='about'),
    path('subscribe/', subscribe, name='subscribe'),
    path('pay/', views.pay, name='pay'),
    path('stk/', views.stk, name='stk'),
    
]
