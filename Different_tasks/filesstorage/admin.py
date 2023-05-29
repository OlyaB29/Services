from django.contrib import admin

from . models import MyFiles

@admin.register(MyFiles)
class MyFilesAdmin(admin.ModelAdmin):

    list_display = ('id', 'myfile')
