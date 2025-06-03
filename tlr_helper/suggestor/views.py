from django.shortcuts import render, redirect, get_object_or_404
from .forms import RouteSelectForm, FilterForm, SignUpForm
from .tlr_engine import find_matches
from .models import Tlr, Strand, SubStrand, Subject
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Model
import unicodedata
import re
from django.contrib.auth import login


PINTEREST_BOARDS = [
    {
        "title": "Creative Teaching Aids for KG – Numeracy",
        "url": "https://www.pinterest.com/Ellet_nahc/creative-teaching-aids-for-kg-numeracy/",
    },
    {
        "title": "KG Literacy Visuals & Games",
        "url": "https://www.pinterest.com/Ellet_nahc/kg-literacy-visuals-games/",
    },
    {
        "title": "Our World – Nature and Environment",
        "url": "https://www.pinterest.com/Ellet_nahc/our-world--nature-and-environment/",
    },
    {
        "title": "Arts and Crafts for Class Activities",
        "url": "https://www.pinterest.com/Ellet_nahc/arts-and-crafts-for-class-activities/",
    },
    {
        "title": "Assessment Tools and DIY Materials",
        "url": "https://www.pinterest.com/Ellet_nahc/assessment-tools-and-diy-materials/",
    },
    {
        "title": "Inclusive Classrooms – Special Needs",
        "url": "https://www.pinterest.com/Ellet_nahc/inclusive-classrooms-special-needs/",
    },
    {
        "title": "Classroom Setup and Resource Displays",
        "url": "https://www.pinterest.com/Ellet_nahc/classroom-setup-and-resource-displays/",
    },
]


def normalize(text):
    if not isinstance(text, str):
        text = str(text)
    text = unicodedata.normalize('NFKD', text).lower()
    return re.sub(r'[^a-z0-9 ]+', '', text)

@login_required
def download_view(request, pk):
    tlr = get_object_or_404(Tlr, pk=pk)
    content = (
        f"{tlr.title}\n\n"
        f"Purpose: {tlr.brief_description}\n"
        f"Materials: {', '.join(m.name for m in tlr.materials.all())}\n"
        f"Time Required: {tlr.get_time_needed_display() if tlr.time_needed else 'N/A'}\n"
        f"Budget Range: {tlr.get_budget_band_display() if tlr.budget_band else 'N/A'}\n"
        f"Bloom Level: {tlr.get_bloom_level_display() if tlr.bloom_level else 'N/A'}\n"
        f"Special Needs: {', '.join(n.name for n in tlr.special_needs.all())}\n"
        f"Learning Styles: {', '.join(l.name for l in tlr.learning_styles.all())}\n\n"
        "Steps to make:\n"
        f"{tlr.steps_to_make}\n\n"
        "Classroom tips:\n"
        f"{tlr.tips_for_use}"
    )
    response = HttpResponse(content, content_type="text/plain")
    safe_title = re.sub(r'[^\w\s-]', '', tlr.title).strip().replace(' ', '_')
    response["Content-Disposition"] = f'attachment; filename="{safe_title}.txt"'
    return response


def load_strands(request):
    class_id = request.GET.get("class_level")
    subject_id = request.GET.get("subject")
    term = request.GET.get("term")
    form = FilterForm()

    if class_id and subject_id and term:
        form.fields["strand"].queryset = Strand.objects.filter(
            subject__class_level_id=class_id,
            subject_id=subject_id,
            term=term
        )
    else:
        form.fields["strand"].queryset = Strand.objects.none()

    return render(request, "partials/strand_options.html", {"form": form})



def load_substrands(request):
    strand_id = request.GET.get("strand")
    subs = SubStrand.objects.filter(strand_id=strand_id)
    html = render_to_string("partials/substrand_options.html", {"subs": subs})
    return HttpResponse(html)


def load_subjects(request):
    class_id = request.GET.get("class_level")
    form = FilterForm()

    if class_id:
        form.fields["subject"].queryset = Subject.objects.filter(class_level_id=class_id)
    else:
        form.fields["subject"].queryset = Subject.objects.none()

    return render(request, "partials/form_field_wrapper.html", {"field": form["subject"]})



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

def route_select(request):
    if request.method == "POST":
        form = RouteSelectForm(request.POST)
        if form.is_valid():
            route = form.cleaned_data["route"]
            return redirect(f"/filters/?route={route}")
    else:
        form = RouteSelectForm()

    return render(request, "route_select.html", {"form": form})


def about_page(request):
    return render(request, "about.html")

@login_required
def print_view(request, pk):
    tlr = get_object_or_404(Tlr, pk=pk)
    return render(request, "print_tlr.html", {"tlr": tlr})


def serialize_filters(data):
    safe = {}
    for key, value in data.items():
        if isinstance(value, Model):
            safe[key] = value.pk
        elif hasattr(value, "__iter__") and not isinstance(value, str):
            safe[key] = [obj.pk if isinstance(obj, Model) else obj for obj in value]
        else:
            safe[key] = value
    return safe

@login_required
def filter_page(request):
    route = request.GET.get("route")
    if not route:
        return redirect("route_select")  

    if request.method == "POST":
        form = FilterForm(request.POST)
        if form.is_valid():
            request.session["filters"] = serialize_filters(form.cleaned_data)   # stash in session
            request.session["route"]   = route
            return redirect("results_page")
    else:
        form = FilterForm()

    return render(request, "filter_form.html",
                  {"form": form, "route": route})

@login_required
def results_page(request):
    filters = request.session.get("filters")
    route   = request.session.get("route")
    if not filters or not route:
        return redirect("route_select")

    suggestions = find_matches(filters, route)

    def normalize(text):
        if not isinstance(text, str):
            text = str(text)
        text = unicodedata.normalize('NFKD', text).lower()
        return re.sub(r'[^a-z0-9 ]+', '', text)

    # Collect all keywords from filters and suggestions
    keywords = set()

    for key in ["class_level", "subject", "strand", "substrand", "intended_use"]:
        val = filters.get(key)
        if val:
            text = getattr(val, "title", None) or getattr(val, "name", None) or str(val)
            stopwords = {"the", "and", "or", "for", "to", "in", "on", "of", "with", "by", "at", "a", "an", "from"}
            words = [w for w in normalize(text).split() if w not in stopwords]
            keywords.update(words)


    for tlr in suggestions:
        for tag_group in [
            tlr.themes.all(),
            tlr.key_learning_areas.all(),
            tlr.resource_types.all(),
            tlr.competencies.all(),
            tlr.special_needs.all(),
            tlr.learning_styles.all()
        ]:
            for tag in tag_group:
                keywords.update(normalize(str(tag)).split())

    # Match all boards that overlap with any keyword
    stopwords = {"the", "and", "or", "for", "to", "in", "on", "of", "with", "by", "at", "a", "an", "from"}

    matched_boards = []
    for board in PINTEREST_BOARDS:
        title_words = set(normalize(board["title"]).split())
        match = keywords & title_words
        filtered_match = [w for w in match if w not in stopwords]
        if filtered_match:
            matched_boards.append({
                "url": board["url"],
                "title": board["title"],
                "matched_words": ", ".join(filtered_match)
            })


    return render(request, "results.html", {
        "suggestions": suggestions,
        "pinterest_boards": matched_boards,
    })


@login_required
def chained_filter(request):
    class_level_id = request.GET.get("class_level")
    subjects = Subject.objects.filter(class_level_id=class_level_id).values("id", "title")
    return JsonResponse(list(subjects), safe=False)

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('route_select')
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})
