from django.contrib import admin
from .models import Post,Comment



class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug','publish')
    list_filter = ('status', 'created', 'publish')
    search_fields = ('title','body')
    prepopulated_fields = {'slug': ('title',)} #prepopulates the slugfield with the title input
    raw_id_fields = ('author',)
    date_hierarchy =  'publish'
    ordering = ('status', 'publish')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email','post','created','active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name','email', 'body')
   


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

