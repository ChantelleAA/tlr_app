from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .forms import RouteSelectForm, FilterForm
from .tlr_engine import find_matches
from .models import *
from django.http import HttpResponse
from django.template.loader import render_to_string

# def query_view(request):
#     if request.method == "POST":
#         form = TLRQueryForm(request.POST)
#         if form.is_valid():
#             suggestions = find_matches(form.cleaned_data)
#             return render(
#                 request,
#                 "results.html",
#                 {"form": form, "suggestions": suggestions},
#             )
#     else:
#         form = TLRQueryForm()
#     return render(request, "query.html", {"form": form})


def download_view(request, pk):
    tlr = get_object_or_404(Tlr, pk=pk)
    content = (
        f"{tlr.title}\n\n"
        f"Purpose: {tlr.brief_description}\n"
        f"Materials: {', '.join(m.name for m in tlr.materials.all())}\n"
        f"Time Needed: {tlr.get_time_needed_display()}\n\n"
        "Steps to make:\n"
        f"{tlr.steps_to_make}\n\n"
        "Classroom tips:\n"
        f"{tlr.tips_for_use}"
    )
    response = HttpResponse(content, content_type="text/plain")
    response["Content-Disposition"] = f'attachment; filename="{tlr.title}.txt"'
    return response

def load_strands(request):
    class_id = request.GET.get("class_level")
    strands = Strand.objects.filter(class_level_id=class_id)
    html = render_to_string("partials/strand_options.html", {"strands": strands})
    return HttpResponse(html)

def load_substrands(request):
    strand_id = request.GET.get("strand")
    subs = SubStrand.objects.filter(strand_id=strand_id)
    html = render_to_string("partials/substrand_options.html", {"subs": subs})
    return HttpResponse(html)


def load_subjects(request):
    class_level_id = request.GET.get('class_level')
    form = FilterForm()
    if class_level_id:
        form.fields['subject'].queryset = Subject.objects.filter(class_level_id=class_level_id)
    else:
        form.fields['subject'].queryset = Subject.objects.none()
    return render(request, "partials/subject_options.html", {"filter_form": form})

def pick_route(request):
    form = RouteSelectForm()
    return render(request, "route_select.html", {"route_form": form})

def show_filters(request):
    route = request.POST.get("route")
    filter_form = FilterForm()
    return render(
        request, "filter_form.html",
        {"filter_form": filter_form, "route": route}
    )

def suggest(request):
    form = FilterForm(request.POST)
    route = request.POST.get("route")  # hidden input
    if form.is_valid():
        suggestions = find_matches(form.cleaned_data, route)
        return render(request, "results.html", {"suggestions": suggestions})
    # redisplay
    return render(request, "filter_form.html", {"filter_form": form, "route": route})