from django.contrib import admin
from .models import Intent, Example

# Register your models here.

class ExampleInline(admin.TabularInline):
  model = Example
  extra = 10

class IntentAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': ['name']})
  ]
  inlines = [ExampleInline]

admin.site.register(Intent, IntentAdmin)