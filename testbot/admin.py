from django.contrib import admin
from .models import Intent, Example, Topic

# Register your models here.


class ExampleInline(admin.TabularInline):
    model = Example
    extra = 10


class IntentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'topic']})
    ]
    list_display = ['name', 'topic']
    list_editable = ['topic']
    inlines = [ExampleInline]


admin.site.register(Intent, IntentAdmin)
admin.site.register(Topic)
