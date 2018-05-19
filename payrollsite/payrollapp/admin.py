from django.contrib import admin

from .models import *

admin.site.register(UserMetaData)
admin.site.register(Expenses)
admin.site.register(PaycheckInformation)

admin.site.register(TimeSheetEntry)
admin.site.register(TimeSheetApprovals)

admin.site.register(PaidTimeOffEntry)
admin.site.register(PaidTimeOffApproval)
admin.site.register(PaidTimeOffHours)
