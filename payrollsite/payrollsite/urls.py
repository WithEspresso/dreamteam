from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Pattern matches from payrollapp.urls if this url is found.
    path('', include('payrollapp.urls')),
    # URL to the admin panel.
    url(r'^admin/', admin.site.urls),
]
