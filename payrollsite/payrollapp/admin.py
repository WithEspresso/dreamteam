from django.contrib import admin

from .models import *

admin.site.register(UserMetaData)
admin.site.register(ExpenseRequest)
admin.site.register(PaidTimeOffRequests)
