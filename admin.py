from django.contrib import admin
from .models import Blog,Comment,Profile
# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    list_display = ['title','context','category','created_date','update_date']
    list_filter = ['title','category']
    search_fields = ['title','category']


admin.site.register(Blog,BlogAdmin)
admin.site.register(Comment)
admin.site.register(Profile) 