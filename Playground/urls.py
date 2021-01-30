from django.urls import path
from . import views
urlpatterns = [
    path("",views.playground,name="playground"),
    path("share/<token>/",views.share,name="share"),
    path("embed/<token>/",views.embed,name="embed"),
    # path("<id>/",views.rendering,name="rendering"),
    path('create/<var>/',views.emptyplay,name="emptyplay"),
    path('savefile/<id>/',views.savefile,name="savefile"),
    path('save/<id>/',views.save,name="save"),
    path('temp/<id>/',views.temp,name="temp"),
    path('test/',views.test,name="test"),
    path('switch/live/',views.live,name="live"),





    #----------------------------- Frontend ---------------------------------------

    path("frontend/create/<var>/",views.frontend,name="frontend"),
    path("frontend/load/",views.load,name="load"),
    path("frontend/template/load/",views.template_load,name="template_load"),
    path("frontend/get/",views.frontend_run,name="run"),
]