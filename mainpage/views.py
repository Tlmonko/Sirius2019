from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from PIL import Image
from django.conf import settings


def index(request):
    if request.method == "POST":
        uploaded_file = request.FILES['picture']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        image = Image.open(settings.MEDIA_ROOT + "/" + uploaded_file.name)
        image.thumbnail((500, 500), Image.NEAREST)
        image.save(settings.MEDIA_ROOT + "/" + uploaded_file.name.split(".")[0] + "_min" + "." +
                   uploaded_file.name.split(".")[1])
    return render(request, "Html/mainpage.html")
