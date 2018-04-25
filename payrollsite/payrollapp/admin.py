from django.contrib import admin

from .models import *

admin.site.register(UserMetaData)
admin.site.register(Expenses)
admin.site.register(PaidTimeOffRequests)
admin.site.register(PaycheckInformation)
admin.site.register(TimeSheetSubmission)
admin.site.register(PaidTimeOffHours)