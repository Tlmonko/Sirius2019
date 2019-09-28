from django.shortcuts import render
from django.core.files.storage import FileSystemStorage


def index(request):
    if request.method == "POST":
        uploaded_file = request.FILES['picture']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
    return render(request, "Html/mainpage.html")
