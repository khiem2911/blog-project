from django.contrib import admin
from .models import UserProfile,Post,Comment
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at','updated_at') 
admin.site.register(UserProfile)
admin.site.register(Post,PostAdmin)
admin.site.register(Comment)

