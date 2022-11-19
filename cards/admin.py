from django.contrib import admin
from .models import Card

# Register your models here.

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('question', 'box')



