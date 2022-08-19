from xml.etree.ElementTree import Comment
from django.contrib import admin
from .models import Board, Answer, FreeBoard, FreeAnswer
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Board)
class BoardAdmin(SummernoteModelAdmin):
    summernote_fields = ('contents',)
    list_display = (
        'title',
        'contents',
        'writer',
        'board_name',
        'hits',
        'write_dttm',
        'update_dttm'
    )
    list_display_links = list_display

admin.site.register(Answer)

@admin.register(FreeBoard)
class FreeBoardAdmin(SummernoteModelAdmin):
    summernote_fields = ('contents',)
    list_display = (
        'title',
        'contents',
        'writer',
        'board_name',
        'hits',
        'write_dttm',
        'update_dttm'
    )
    list_display_links = list_display

admin.site.register(FreeAnswer)