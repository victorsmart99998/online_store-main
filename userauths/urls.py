from django.urls import path

from . import views

app_name = 'userauths'

urlpatterns = [
    # Leave as empty string for base url
    path('sign_up/', views.register_view, name="sign_up"),
    path('sign_in/', views.login_view, name="sign_in"),

]
