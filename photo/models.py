from django.db import models
from django.urls import reverse
# 사진에 대한 원본 이미지와 썸네일 이미지를 모두 저장할 수 있는 커스텀 필드
from photo.field import ThumbnailImageField


# class Album(models.Model):
#     name = models.CharField(max_length=30)
#     description = models.CharField('One Line Description', max_length=100, blank=True)

#     class Meta:
#         ordering = ('name',) # 객체 리스트를 출력할때 정렬 기준

#     def __str__(self):
#         return self.name

#     # 이 메소드가 정의된 객체를 지칭하는 URL을 반환
#     # /photo/album/99
#     def get_absolute_url(self):
#         return reverse('photo:album_detail', args=(self.id,))

# class Photo(models.Model):
#     # 외래키
#     album = models.ForeignKey(Album,on_delete=models.CASCADE)
#     title = models.CharField('TITLE',max_length=30)
#     description = models.TextField('Photo Description',blank=True)
#     image = ThumbnailImageField(upload_to='photo/%Y/%m')
#     upload_dt = models.DateTimeField('Upload Date', auto_now=True)

#     class Meta:
#         ordering = ('title',)

#     def __str__(self):
#         return self.title

#     def get_absolute_url(self):
#         return reverse('photo:photo_detail', args=(self.id,))


class FileUpload(models.Model):
    title = models.TextField(max_length=40, null=True)
    imgfile = models.ImageField(null=True, upload_to="", blank=True)
    content = models.TextField()

    def __str__(self):
        return self.title