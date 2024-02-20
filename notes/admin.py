from django.contrib import admin
from notes.models import Note, NoteVersion

# Register your models here.
class NotesAdmin(admin.ModelAdmin):
    list_display = ('user', 'title')  # Fields to display in the list view
    search_fields = ('user', 'title')  # Fields to enable searching
    list_filter = ('user',)  # Fields to enable filtering

admin.site.register(Note, NotesAdmin)