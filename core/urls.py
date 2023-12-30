
from django.urls import path
from core import views

urlpatterns = [
    #path pour la page home
    path('',views.home,name="home")
]
