from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .forms import TLRQueryForm
from .tlr_engine import find_matches
from .models import Tlr
from django.http import HttpResponse
from django.template.loader import render_to_string

def query_view(request):
    if request.method == "POST":
        form = TLRQueryForm(request.POST)
        if form.is_valid():
            suggestions = find_matches(form.cleaned_data)
            return render(
                request,
                "results.html",
                {"form": form, "suggestions": suggestions},
            )
    else:
        form = TLRQueryForm()
    return render(request, "query.html", {"form": form})


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