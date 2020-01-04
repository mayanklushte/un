from django.contrib import admin
from register_app.models import pat_register, doc_register, pat_details, R_appoint, pat_report
# Register your models here.
admin.site.register(pat_register)
admin.site.register(doc_register)
admin.site.register(pat_details)
admin.site.register(R_appoint)
admin.site.register(pat_report)
