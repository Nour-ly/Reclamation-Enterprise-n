from django.contrib import admin
from .models import Category, Complaint, Profile

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)

admin.site.register(Category)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Complaint)
