"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from suggestor import views as v

urlpatterns = [
    path("admin/", admin.site.urls),
    path("download/<int:pk>/", v.download_view, name="download"),
    path("ajax/strands/", v.load_strands, name="ajax_load_strands"),
    path("ajax/substrands/", v.load_substrands, name="ajax_load_substrands"),
    path("", v.pick_route, name="pick_route"),
    path("filters/", v.show_filters, name="show_filters"),
    path("suggest/", v.suggest, name="suggest"),
    path('chaining/', include('smart_selects.urls')),
    path("load-subjects/", v.load_subjects, name="load_subjects"),
]
