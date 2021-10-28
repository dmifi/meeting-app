from django.contrib import admin
from users.models import Client, Match


@admin.register(Client)
class Client(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'sex', 'is_active', 'is_staff')


@admin.register(Match)
class ClientMatching(admin.ModelAdmin):
    list_display = ('from_match', 'to_match')
