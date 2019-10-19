from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from PIL import Image
from django.http import JsonResponse
from django.conf import settings
from .models import Picture
import os


def get_images(request):
    count_of_pictures = int(request.GET["images"])
    pictures = Picture.objects.all()
    if len(pictures) >= count_of_pictures + 6:
        pictures = pictures[count_of_pictures:count_of_pictures + 6]
    else:
        pictures = pictures[count_of_pictures:]
    images = list(map(
            lambda image: {
                'id': image.id,
                'name': image.name,
                'path': image.path,
                'path_thumbnails': image.path_thumbnails
            },
            pictures
        ))
    return JsonResponse({"images": images}, safe=False)

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
            pictures = Picture.objects.all()
            new_object_params = {"path": "/media/" + uploaded_file.name,
                                "path_thumbnails": "/media/" + ".".join(uploaded_file.name.split(".")[:-1]) + "_min" + "." +
                                                    uploaded_file.name.split(".")[-1], "name": uploaded_file.name}

            Picture.objects.create(**new_object_params)
    elif request.method == "GET":
        if "id" in request.GET:
            obj = Picture.objects.get(id=int(request.GET["id"]))
            path = settings.MEDIA_ROOT[:-6] + obj.path
            path_min = settings.MEDIA_ROOT[:-6] + ".".join(obj.path.split(".")[:-1]) + "_min" + "." + obj.path.split(".")[-1]
            obj.delete()
            if os.path.isfile(path) and os.path.isfile(path_min):
                os.remove(path)
                os.remove(path_min)
    pictures = Picture.objects.all()
    count_of_pictures = 0
    if isBe:
        return render(request, "Html/mainpage.html", {"param": "Картинка с таким названием уже существует!"})
    else:
        return render(request, "Html/mainpage.html", {"param": ""})
