from django.urls import path
from photo import views

app_name = 'photo'

urlpatterns=[
    # # /photo/
    # path('', views.AlbumLV.as_view(),name='index'),
    # # path('', views.AlbumLV.as_view(model=Album), name='index'), # 이렇게 정의하면 views.py 에 따로 코딩안해도 된다.

    # path('album',views.AlbumLV.as_view(), name='album_list'),

    # path('album/<int:pk>/', views.AlbumDV.as_view(), name='album_detail'),

    # path('photo/<int:pk>/', views.PhotoDV.as_view(), name='photo_detail')

    path('fileupload/', views.fileUpload, name="fileupload"),
]