from django.urls import path

from .views import homePageView,greg,samplepacks,appScriptScreenShot

urlpatterns = [
    path("", homePageView, name="home"),
    path("greg", greg, name="greg"),
    path("samplepacks", samplepacks, name="samplepacks"),
    path("appScriptScreenShot", appScriptScreenShot, name="appScriptScreenShot"),

]