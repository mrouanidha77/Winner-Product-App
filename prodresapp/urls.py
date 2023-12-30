
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    #j ai ajouter ce path pour qu il doit iclure urls.py de l application core 
    path('',include('core.urls'))
]
