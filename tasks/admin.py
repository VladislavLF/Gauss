from django.contrib import admin
from .models import *


class Category_Tasks_Filter_Admin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'condition_preview', 'cat', 'filter', 'is_published')
    list_filter = ('cat', 'filter', 'is_published')
    search_fields = ('condition', 'solution', 'answer')

    def condition_preview(self, obj):
        return obj.condition[:100] + '...' if len(obj.condition) > 100 else obj.condition

    condition_preview.short_description = 'Condition Preview'


class Category_OptionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'difficult', 'is_published')
    list_filter = ('difficult', 'is_published')
    search_fields = ('description',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post_preview', 'created', 'is_published')
    list_filter = ('is_published', 'created')
    search_fields = ('text', 'user__username')

    def post_preview(self, obj):
        return obj.post.condition[:50] + '...' if len(obj.post.condition) > 50 else obj.post.condition

    post_preview.short_description = 'Task Preview'


admin.site.register(Task, TaskAdmin)
admin.site.register(Category_Options, Category_OptionsAdmin)
admin.site.register(Category_Tasks)
admin.site.register(Theory_item)
admin.site.register(Theory_category)
admin.site.register(Category_Tasks_Filter, Category_Tasks_Filter_Admin)
admin.site.register(Comment, CommentAdmin)
