from django.shortcuts import render, get_object_or_404
from .forms import RouteSelectForm, FilterForm
from .tlr_engine import find_matches
from .models import *
from django.http import HttpResponse, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST


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
    class_id = request.GET.get("subject")
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
    route = request.GET.get("route")
    filter_form = FilterForm()
    return render(
        request, "filter_form.html",
        {"filter_form": filter_form, "route": route}
    )

@require_POST
def suggest(request):
    form  = FilterForm(request.POST)
    route = request.POST.get("route")

    if form.is_valid():
        suggestions = find_matches(form.cleaned_data, route)

        # HTMX? -> return only the snippet
        if request.headers.get("HX-Request") == "true":
            html = render_to_string("partials/results_list.html",
                                    {"suggestions": suggestions},
                                    request=request)
            return HttpResponse(html)

        # non-JS fallback
        return render(request, "results.html", {"suggestions": suggestions})

    # invalid form
    if request.headers.get("HX-Request") == "true":
        return HttpResponseBadRequest("Form invalid")
    return render(request, "filter_form.html",
                  {"filter_form": form, "route": route})