

from django.contrib import admin
from .models import JobPosts, Date
from import_export.admin import ImportExportActionModelAdmin, ImportExportMixin, ImportMixin

# Register your models here.



from import_export import resources

class JobPostsResource(resources.ModelResource):

    class Meta:
        model = JobPosts


class JobPostsAdmin(ImportExportActionModelAdmin):
    pass


admin.site.register(JobPosts, JobPostsAdmin)
admin.site.register(Date)