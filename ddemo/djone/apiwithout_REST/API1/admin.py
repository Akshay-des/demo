from django.contrib import admin
from API1.models import Employee
# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id','eno','ename','esal','eaddr']

admin.site.register(Employee,EmployeeAdmin)