from django.contrib import admin
from .models import *

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'image', 'first_name', 'last_name', 'phone_number']
    fields = ['email', 'first_name', 'image', 'last_name', 'phone_number']

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'description', 'created_at']
    fields = ['user', 'title', 'description', 'image']
    search_fields = ('title', 'description',)
    raw_id_fields = ('user',)


@admin.register(BlogImage)
class  BlogImageAdmin(admin.ModelAdmin):
    list_display = ['blog', 'image', 'is_main', 'created_at']
    fields = ['blog', 'image', 'is_main']
    row_id_fields = ('blog',)

@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'blog', 'comment', 'created_at']
    fields = ['user', 'blog', 'comment']
    search_fields = ('user', 'blog')
    row_id_fields = ('user', 'blog',)

    # list_display = ['comment', 'created_at']
    # fields = ['comment']
    # # search_fields = ('user', 'blog')
    # # row_id_fields = ('user', 'blog',)




    
