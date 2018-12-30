from django.contrib import admin

# Register your models here.
from scholarship.models import Scholarship


class ScholarshipAdmin(admin.ModelAdmin):
    pass


admin.site.register(Scholarship, ScholarshipAdmin)
