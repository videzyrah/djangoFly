from django.contrib import admin
from .models import Department, Item

admin.site.register(Department)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('writtenId', 'name', 'status', 'borrower', 'due_back')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('writtenId', 'name', 'image', 'donor', 'department', 'condition')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )
