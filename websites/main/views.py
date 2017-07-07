from django.shortcuts import render
from django.http import Http404, HttpResponse

def custom_404(request):
    return render(request, 'websites/errors/404.html', {}, status=404)

def custom_500(request):
    return render(request, 'websites/errors/500.html', {}, status=500)