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
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Authentication
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    path("admin/",      admin.site.urls),
    path("chained-filter/", v.chained_filter, name="chained_filter"),

    # Welcome page
    path("",            v.welcome_page, name="welcome"),
    
    # 3-step flow
    path("search/",     v.route_select, name="route_select"),
    path("filters/",    v.filter_page,  name="filter_page"),
    path("results/",    v.results_page, name="results_page"),

    # downloads
    path("download/<int:pk>/", v.download_view, name="download_tlr"),

    # AJAX endpoints
    path("ajax/subjects/",     v.ajax_load_subjects,     name="ajax_load_subjects"),
    path("ajax/strands/",      v.ajax_load_strands,      name="ajax_load_strands"),
    path("ajax/substrands/",   v.ajax_load_substrands,   name="ajax_load_substrands"),

    # Pages
    path("about/", v.about_page, name="about"),
    path("contact/", v.contact_page, name="contact"),  # NEW
    path("print/<int:pk>/", v.print_view, name="print_tlr"),
    path("signup/", v.signup_view, name="signup"),
    path("tlr/<slug:slug>/", v.tlr_detail_page, name="tlr_detail"),
    path('chained/', include('smart_selects.urls')),
    path('api/activity/', v.activity_api, name='activity_api'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)