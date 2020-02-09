from django.contrib import admin
from APIVSdemo.models import Employee

# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id','eno','esal','eaddr','ename']

admin.site.register(Employee,EmployeeAdmin)