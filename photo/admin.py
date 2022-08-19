from django.contrib import admin
# from photo.models import Album, Photo
from photo.models import FileUpload
# # StackedInline : 세로로 나열
# class PhotoInline(admin.StackedInline):
#     model = Photo
#     extra = 2        # 이미 존재하는 객체 외에 추가로 입력할 수 있는 photo 테이블 객체 수는 2개

# @admin.register(Album)
# class AlbumAdmin(admin.ModelAdmin):
#     inlines = (PhotoInline,)
#     list_display = ('id','name','description')

# @admin.register(Photo)
# class PhotoAdmin(admin.ModelAdmin):
#     list_display = ('id','title','upload_dt')

admin.site.register(FileUpload)