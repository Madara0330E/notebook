from django.contrib import admin
from .models import Person, Contact, Relationship, Event, GreetingTemplate, Greeting

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'patronymic', 'birth_date', 'workplace', 'position')
    search_fields = ('last_name', 'first_name', 'patronymic')
    list_filter = ('gender', 'workplace')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('person', 'phone', 'email', 'updated_at')
    search_fields = ('person__last_name', 'phone', 'email')
    list_filter = ('updated_at',)

@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    list_display = ('person', 'relationship_type', 'related_person')
    search_fields = ('person__last_name', 'related_person__last_name')
    list_filter = ('relationship_type',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('person', 'event_type', 'event_date', 'reminder_days')
    search_fields = ('person__last_name', 'event_type')
    list_filter = ('event_type', 'event_date')

@admin.register(GreetingTemplate)
class GreetingTemplateAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'template_text')
    search_fields = ('event_type',)

@admin.register(Greeting)
class GreetingAdmin(admin.ModelAdmin):
    list_display = ('person', 'event', 'created_at', 'is_sent')
    search_fields = ('person__last_name', 'greeting_text')
    list_filter = ('is_sent', 'created_at')
    readonly_fields = ('created_at',)
