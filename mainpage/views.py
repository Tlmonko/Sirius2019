from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from PIL import Image
from django.conf import settings
from .models import Picture
import os


def index(request):
    isBe = False
    if request.method == "POST":
        uploaded_file = request.FILES['picture']
        fs = FileSystemStorage()
        if os.path.isfile(settings.MEDIA_ROOT + "/" + uploaded_file.name):
            isBe = True
        else:
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
            image.save(settings.MEDIA_ROOT + "/" + ".".join(uploaded_file.name.split(".")[:-1]) + "_min" + "." +
                    uploaded_file.name.split(".")[-1])
            new_object_params = {"path": "/media/" + uploaded_file.name,
                                "path_thumbnails": "/media/" + ".".join(uploaded_file.name.split(".")[:-1]) + "_min" + "." +
                                                    uploaded_file.name.split(".")[-1], "name": uploaded_file.name}

            Picture.objects.create(**new_object_params)
    elif request.method == "GET":
        if "image" in request.GET:
            print(request.GET)
            obj = Picture.objects.get(path="/media/" + request.GET["image"])
            obj.delete()
            path = settings.MEDIA_ROOT + "/" + request.GET["image"]
            path_min = settings.MEDIA_ROOT + "/" + ".".join(request.GET["image"].split(".")[:-1]) + "_min" + "." + request.GET["image"].split(".")[-1]
            print(path, path_min)
            if os.path.isfile(path) and os.path.isfile(path_min):
                os.remove(path)
                os.remove(path_min)
    pictures = Picture.objects.all()
    if isBe:
        return render(request, "Html/mainpage.html", {"pictures_list": pictures, "param": "Картинка с таким названием уже существует!"})
    else:
        return render(request, "Html/mainpage.html", {"pictures_list": pictures, "param": ""})
