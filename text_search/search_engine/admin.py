from django.contrib import admin
from search_engine.models import *


class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'pages_number', 'author', 'year']
    list_display_links = ['title']
    # fields = (('name', 'surname'), 'email', 'address', 'phone')
    # list_per_page = 10
    # search_fields = ('name', 'surname', 'email', 'phone', 'address',)


class PageAdmin(admin.ModelAdmin):
    list_display = ['number', 'part_name', 'section_name', 'chapter_name', 'book']
    list_display_links = ['number', 'part_name']


admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Page, PageAdmin)
