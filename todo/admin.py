from django.contrib import admin
from .models import TodoItem, Comment

@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_on')
    prepopulated_fields = {"slug":('title',)}

admin.site.register(Comment)
