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

# urlpatterns = [
#     # Authentication
#     path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
#     path("logout/", auth_views.LogoutView.as_view(), name="logout"),

#     path("admin/",      admin.site.urls),
#     path("chained-filter/", v.chained_filter, name="chained_filter"),

#     # Welcome page (new)
#     path("",            v.welcome_page, name="welcome"),           # NEW: Landing page
    
#     # 3-step flow (updated paths)
#     path("search/",     v.route_select, name="route_select"),     # step-1: Choose route
#     path("filters/",    v.filter_page,  name="filter_page"),      # step-2: Set filters  
#     path("results/",    v.results_page, name="results_page"),     # step-3: View results

#     # downloads
#     path("download/<int:pk>/", v.download_view, name="download_tlr"),

#     # AJAX endpoints
#     path("ajax/subjects/",     v.load_subjects,     name="ajax_load_subjects"),
#     path("ajax/strands/",      v.load_strands,      name="ajax_load_strands"),
#     path("ajax/substrands/",   v.load_substrands,   name="ajax_load_substrands"),

#     # Extras
#     path("about/", v.about_page, name="about"),
#     path("print/<int:pk>/", v.print_view, name="print_tlr"),
#     path("signup/", v.signup_view, name="signup"),
# ]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

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
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)