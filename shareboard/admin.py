from xml.etree.ElementTree import Comment
from django.contrib import admin
from .models import ShareBoard, ShareAnswer
from django_summernote.admin import SummernoteModelAdmin

@admin.register(ShareBoard)
class ShareBoardAdmin(SummernoteModelAdmin):
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

admin.site.register(ShareAnswer)

