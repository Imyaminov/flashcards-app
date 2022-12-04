from django.contrib import admin
from .models import (
    Card,
    StudySet,
    Folder,
)

# Register your models here.

class CardInline(admin.TabularInline):
    model = Card

class StudySetInline(admin.TabularInline):
    model = StudySet

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('question', 'box')

@admin.register(StudySet)
class StudySetAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'author')
    inlines = (
        CardInline,
    )

@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'author')
    inlines = (
        StudySetInline,
    )


