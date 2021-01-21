from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("changePassword", views.changePassword, name="changePassword"),

    path('subscribe', views.subscribe, name="subscribe"),


    path('phoneDetailView', views.phoneDetailView, name="phoneDetailView"),
    path('createPhone', views.createPhone, name="createPhone"),
    path('deletePhone/<id>', views.deletePhone, name="deletePhone"),

    path('addressDetailView', views.addressDetailView, name="addressDetailView"),
    path('createAddress', views.createAdrress, name="createAddress"),
    path('updateAddress/<id>', views.updateAddress, name="updateAddress"),
    path('setPrimaryAddress/<id>', views.setPrimaryAddress, name="setPrimaryAddress"),
    path('deleteAddress/<id>', views.deleteAddress, name="deleteAddress"),
]