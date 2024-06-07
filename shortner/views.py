from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import urls
import string
import random
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

def index(request):
    return render(request,"index.html")
def generate_unique_id():
    length = 8
    characters = string.ascii_letters + string.digits
    while True:
        unique_id = ''.join(random.choice(characters) for _ in range(length))
        if not urls.objects.filter(uid=unique_id).exists():
            return unique_id
def create(request):
    if request.method == "POST":
        link = request.POST.get('link')
        if link:
            validator = URLValidator()
            try:
                validator(link)
            except ValidationError:
                return HttpResponse("Invalid URL.", status=400)
            base_url = f"{request.scheme}://{request.get_host()}"
            uid = generate_unique_id()
            urls.objects.create(url=link, uid=uid)
            return HttpResponse(base_url + "/" + str(uid))
        return HttpResponse("URL field is required.")
    return HttpResponse("Invalid request method.")
def go(request,id):
    try:
        url = urls.objects.get(uid = id)
        return redirect(url.url)
    except urls.DoesNotExist:
        return render(request,"404.html")


    