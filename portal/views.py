from django.shortcuts import render

from django.http import HttpResponse


def homePageView(request):
    return render(request, 'index.html')

def greg(request):
    return HttpResponse("Greg!")

def samplepacks(request):
    return render(request, 'samplepacks.html')

def appScriptScreenShot(request):
    return render(request, 'appScriptScreenShot.html')