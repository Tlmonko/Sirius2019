from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from PIL import Image
from django.conf import settings
from .models import Picture


def index(request):
    if request.method == "POST":
        uploaded_file = request.FILES['picture']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        image = Image.open(settings.MEDIA_ROOT + "/" + uploaded_file.name)

        width, height = image.size
        side = min(width, height)
        left, upper = (width - side) // 2, (height - side) // 2
        right, lower = left + side, upper + side
        print(left, upper, right, lower)
        print(width, height)
        image = image.crop((left, upper, right, lower))

        image.thumbnail((300, 300))
        image.save(settings.MEDIA_ROOT + "/" + uploaded_file.name.split(".")[0] + "_min" + "." +
                   uploaded_file.name.split(".")[-1])
        new_object_params = {"path": "/media/" + uploaded_file.name,
                             "path_thumbnails": "/media/" + uploaded_file.name.split(".")[0] + "_min" + "." +
                                                uploaded_file.name.split(".")[-1], "name": uploaded_file.name}

        Picture.objects.create(**new_object_params)
    pictures = Picture.objects.all()
    return render(request, "Html/mainpage.html", {"pictures_list": pictures})
