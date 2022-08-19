import os
from PIL import Image
from django.db.models.fields.files import ImageField, ImageFieldFile

class TumbnailImageFieldFile(ImageFieldFile):

    # 확장자 수정 메소드
    def _add_thumb(self,file_name):
        parts = file_name.split(".")
        parts.insert(-1, "thumb")

        # 확장자 부분 'jpg' 로 수정
        if parts[-1].lower() not in ['jpeg','jpg']:
            parts[-1] = 'jpg'

        return ".".join(parts)

    # 데코레이터를 사용하여 메소드를 멤버 변수처럼 사용할 수 있다.
    @property
    def thumb_path(self):
        return self._add_thumb(self.path)   # 함수를 리턴

    @property
    def thumb_url(self):
        return self._add_thumb(self.url)

    def save(self,name, content, save=True):
        super().save(name,content,save)     # 부모 메소드 실행, 원본 이미지 저장

        img = Image.open(self.path)

        # 디폴트 128 x 128
        size = (self.field.thumb_width, self.field.thumb_height)
        img.thumbnail(size)
        background = Image.new('RGB', size, (255,255,255))

        # 썸네일 박스에 붙이기
        box = (int((size[0] - img.size[0])/3), int((size[1] - img.size[1])/ 3))
        background.paste(img,box)
        background.save(self.thumb_path, 'JPEG')

    def delete(self, save=True):
        if os.path.exists(self.thumb_path):
            os.remove(self.thumb_path)
        super().delete(save)


class ThumbnailImageField(ImageField):
        attr_class = TumbnailImageFieldFile

        def __init__(self, verbose_name=None, thumb_width=128, thumb_height=128, **kwargs):
            self.thumb_width, self.thumb_height = thumb_width, thumb_height
            super().__init__(verbose_name,**kwargs)