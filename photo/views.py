from django.shortcuts import render, redirect
# from django.views.generic import ListView, DetailView
# from photo.models import Album, Photo
from .forms import FileUploadForm
from .models import FileUpload
# class AlbumLV(ListView):
#     model = Album
#     # {{ object }}

# class AlbumDV(DetailView):
#     model = Album
#     # {{ object_list }}

# class PhotoDV(DetailView):
#     model = Photo

def fileUpload(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        img = request.FILES["imgfile"]
        fileupload = FileUpload(
            title=title,
            content=content,
            imgfile=img,
        )
        fileupload.save()
        return redirect('/photo/fileupload')
    else:
        fileuploadForm = FileUploadForm
        context = {
            'fileuploadForm': fileuploadForm,
        }
        return render(request, 'photo/fileupload.html', context)