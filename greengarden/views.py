from django.shortcuts import render
from django.utils import timezone


def index(request):
    context = {
        'ultimo_escaneo': timezone.now()
    }
    return render(request, "greengarden/index.html", context)
