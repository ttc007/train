from django.shortcuts import render
from django.http import Http404, HttpResponse

def custom_404(request):
    return render(request, 'websites/errors/404.html', {})

def custom_500(request):
    print 'status 500'
    return render(request, 'websites/errors/500.html', {})