from django.shortcuts import render, redirect, get_object_or_404
from .forms import RouteSelectForm, FilterForm, SignUpForm
from .tlr_engine import find_matches
from .models import Tlr, Strand, SubStrand, Subject
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import unicodedata
import re
from django.contrib.auth import login
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm 
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from io import BytesIO
from django.db.models import F, Q, Model
from .forms import EnhancedRouteSelectForm
import openai
import os
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt


@login_required
@csrf_exempt
def activity_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # For now, just return success - we'll enhance this later
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'})

def get_client_ip(request):
    """Get the client's IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

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
    {
        "title": "Nature and Environment Activities",
        "url": "https://www.pinterest.com/Ellet_nahc/kg2-nature-and-environment/",
    }
]

def welcome_page(request):
    """Landing page showing TLR Helper features and pricing"""
    return render(request, 'welcome.html')

def normalize(text):
    if not isinstance(text, str):
        text = str(text)
    text = unicodedata.normalize('NFKD', text).lower()
    return re.sub(r'[^a-z0-9 ]+', '', text)

@login_required
def download_view(request, pk):
    tlr = get_object_or_404(Tlr, pk=pk)

    from .models import UserActivity
    UserActivity.objects.create(
        user=request.user,
        action='download_tlr',
        tlr=tlr,
        ip_address=get_client_ip(request),
        page_url=request.build_absolute_uri()
    )

    from django.db.models import F
    Tlr.objects.filter(pk=pk).update(download_count=F('download_count') + 1)
    
    buffer = BytesIO()
    
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        textColor='#2c3e50'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceBefore=12,
        spaceAfter=6,
        textColor='#34495e'
    )
    
    normal_style = styles['Normal']
    normal_style.fontSize = 10
    normal_style.spaceAfter = 12
    
    # Add content to PDF
    # Title
    title = Paragraph(tlr.title, title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Purpose
    purpose_heading = Paragraph("<b>Purpose</b>", heading_style)
    elements.append(purpose_heading)
    purpose_text = Paragraph(tlr.brief_description or "N/A", normal_style)
    elements.append(purpose_text)
    
    # Materials
    materials = ', '.join(m.name for m in tlr.materials.all()) or "N/A"
    materials_heading = Paragraph("<b>Materials</b>", heading_style)
    elements.append(materials_heading)
    materials_text = Paragraph(materials, normal_style)
    elements.append(materials_text)
    
    # Time Required
    time_heading = Paragraph("<b>Time Required</b>", heading_style)
    elements.append(time_heading)
    time_text = Paragraph(tlr.get_time_needed_display() if tlr.time_needed else 'N/A', normal_style)
    elements.append(time_text)
    
    # Budget Range
    budget_heading = Paragraph("<b>Budget Range</b>", heading_style)
    elements.append(budget_heading)
    budget_text = Paragraph(tlr.get_budget_band_display() if tlr.budget_band else 'N/A', normal_style)
    elements.append(budget_text)
    
    # Bloom Level
    bloom_heading = Paragraph("<b>Bloom Level</b>", heading_style)
    elements.append(bloom_heading)
    bloom_text = Paragraph(tlr.get_bloom_level_display() if tlr.bloom_level else 'N/A', normal_style)
    elements.append(bloom_text)
    
    # Special Needs
    special_needs = ', '.join(n.name for n in tlr.special_needs.all()) or "N/A"
    special_heading = Paragraph("<b>Special Needs</b>", heading_style)
    elements.append(special_heading)
    special_text = Paragraph(special_needs, normal_style)
    elements.append(special_text)
    
    # Learning Styles
    learning_styles = ', '.join(l.name for l in tlr.learning_styles.all()) or "N/A"
    learning_heading = Paragraph("<b>Learning Styles</b>", heading_style)
    elements.append(learning_heading)
    learning_text = Paragraph(learning_styles, normal_style)
    elements.append(learning_text)
    
    # Steps to make
    steps_heading = Paragraph("<b>Steps to Make</b>", heading_style)
    elements.append(steps_heading)
    steps_text = Paragraph(tlr.steps_to_make or "N/A", normal_style)
    elements.append(steps_text)
    
    # Classroom tips
    tips_heading = Paragraph("<b>Classroom Tips</b>", heading_style)
    elements.append(tips_heading)
    tips_text = Paragraph(tlr.tips_for_use or "N/A", normal_style)
    elements.append(tips_text)
    
    # Build PDF
    doc.build(elements)
    
    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    safe_title = re.sub(r'[^\w\s-]', '', tlr.title).strip().replace(' ', '_')
    response['Content-Disposition'] = f'attachment; filename="{safe_title}.pdf"'
    
    return response

def load_subjects(request):
    class_id = request.GET.get("class_level")
    form = FilterForm()

    if class_id:
        form.fields["subject"].queryset = Subject.objects.filter(class_level_id=class_id)
    else:
        form.fields["subject"].queryset = Subject.objects.none()

    return render(request, "partials/form_field_wrapper.html", {"field": form["subject"]})

@login_required
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
    routes = request.session.get("routes", [])
    route = request.session.get("route")
    
    if not routes and route:
        routes = [route]
    elif not routes and not route:
        return redirect("route_select")

    if request.method == "POST":
        form = FilterForm(request.POST)
        print(f"DEBUG filter_page POST: form valid={form.is_valid()}")
        print(f"DEBUG filter_page POST: raw form data={dict(request.POST)}")
        
        if form.is_valid():
            print(f"DEBUG filter_page POST: cleaned_data={form.cleaned_data}")
            print(f"DEBUG filter_page POST: class_level value={form.cleaned_data.get('class_level')}")
            print(f"DEBUG filter_page POST: class_level type={type(form.cleaned_data.get('class_level'))}")
            
            request.session["filters"] = serialize_filters(form.cleaned_data)
            request.session["search_type"] = "advanced"
            request.session["routes"] = routes
            if len(routes) == 1:
                request.session["route"] = routes[0]
            return redirect("results_page")
        else:
            print(f"DEBUG filter_page POST: form errors={form.errors}")
    else:
        form = FilterForm()

    return render(request, "filter_form.html", {
        "form": form, 
        "routes": routes,
        "route": routes[0] if len(routes) == 1 else None
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

def ajax_load_subjects(request):
    class_level_id = request.GET.get("class_level")
    print(f"DEBUG ajax_load_subjects: class_level_id={class_level_id}")
    
    if class_level_id:
        subjects = Subject.objects.filter(class_level_id=class_level_id)
        print(f"DEBUG ajax_load_subjects: found {subjects.count()} subjects: {list(subjects)}")
    else:
        subjects = Subject.objects.none()
        print(f"DEBUG ajax_load_subjects: no class_level_id provided")
    
    return render(request, "partials/subject_dropdown.html", {"subjects": subjects})

def ajax_load_strands(request):
    class_level_id = request.GET.get("class_level")
    subject_id = request.GET.get("subject") 
    term = request.GET.get("term")

    # ... your existing debug code ...

    if class_level_id and subject_id and term and subject_id != '':
        try:
            strands = Strand.objects.filter(
                class_level_id=int(class_level_id),
                subject_id=int(subject_id),
                term=int(term)
            )
            print(f"  Found {strands.count()} strands: {list(strands)}")
        except (ValueError, TypeError) as e:
            print(f"  Error filtering strands: {e}")
            strands = Strand.objects.none()
    else:
        print(f"  Missing required parameters or empty subject")
        strands = Strand.objects.none()

    return render(request, "partials/strand_select.html", {"strands": strands})

def ajax_load_substrands(request):
    strand_id = request.GET.get("strand")
    # Debug prints
    print(f"SUBSTRANDS DEBUG:")
    print(f"  strand_id: {strand_id}")
    
    substrands = SubStrand.objects.none()
    
    if strand_id and strand_id.isdigit():
        try:
            substrands = SubStrand.objects.filter(strand_id=int(strand_id))
            print(f"  Found {substrands.count()} substrands: {list(substrands)}")
        except (ValueError, TypeError) as e:
            print(f"  Error filtering substrands: {e}")
    else:
        print(f"  Invalid or missing strand_id")

    return render(request, "partials/substrand_select.html", {"substrands": substrands})

def contact_page(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Send email
            send_mail(
                subject=f"[{subject.upper()}] Contact Form from {name}",
                message=(
                    f"From: {name}\n"
                    f"Email: {email}\n"
                    f"Phone: {form.cleaned_data.get('phone', '')}\n"
                    f"Organization: {form.cleaned_data.get('organization', '')}\n\n"
                    f"Message:\n{message}"
                ),
                from_email='chantelleope@gmail.com',
                recipient_list=['teddghana@gmail.com', 'support@nileedge.com'],  # Adjust as needed
                fail_silently=False,
            )

            messages.success(
                request, 
                f"Thank you {name}! Your message has been sent. "
                "The TEDD Ghana team will get back to you soon."
            )
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

@login_required
def tlr_detail_page(request, slug):
    tlr = get_object_or_404(Tlr, slug=slug, is_published=True)
    
    # Optional: Track views
    # tlr.view_count = F('view_count') + 1
    # tlr.save(update_fields=['view_count'])
    from .models import UserActivity
    UserActivity.objects.create(
        user=request.user,
        action='view_tlr',
        tlr=tlr,
        ip_address=get_client_ip(request),
        page_url=request.build_absolute_uri()
    )
    # Increment view count
    Tlr.objects.filter(pk=tlr.pk).update(view_count=F('view_count') + 1)
    
    return render(request, "tlr_detail.html", {"tlr": tlr})

@login_required
def route_select(request):
    if request.method == "POST":
        form = EnhancedRouteSelectForm(request.POST)
        if form.is_valid():
            search_type = request.POST.get('search_type')
            
            if search_type == 'keyword':
                # Handle keyword search
                keywords = form.cleaned_data.get('keywords', '').strip()
                if keywords:
                    # Serialize the quick filters properly
                    quick_filters = {}
                    
                    # Handle ClassLevel object
                    if form.cleaned_data.get('class_level'):
                        quick_filters['class_level'] = form.cleaned_data['class_level'].pk
                    
                    # Handle other simple fields
                    if form.cleaned_data.get('time_needed'):
                        quick_filters['time_needed'] = form.cleaned_data['time_needed']
                    
                    if form.cleaned_data.get('budget_band'):
                        quick_filters['budget_band'] = form.cleaned_data['budget_band']
                    
                    # Store in session
                    request.session["search_type"] = "keyword"
                    request.session["keywords"] = keywords
                    request.session["quick_filters"] = quick_filters
                    return redirect("results_page")
            
            elif search_type == 'advanced':
                # Handle advanced route search
                routes = form.cleaned_data.get('routes', [])
                if routes:
                    request.session["search_type"] = "advanced"
                    request.session["routes"] = list(routes)  # Store as list
                    return redirect("filter_page")
            
            # Fallback: if no search type specified, treat as old single route
            route = form.cleaned_data.get('route')  # This might exist if using old form
            if route:
                request.session["routes"] = [route]
                return redirect("filter_page")
    else:
        form = EnhancedRouteSelectForm()

    return render(request, "route_select.html", {"form": form})


@login_required
def results_page(request):
    search_type = request.session.get("search_type")
    
    if search_type == "keyword":
        # Handle keyword search results
        keywords = request.session.get("keywords", "")
        quick_filters_raw = request.session.get("quick_filters", {})
        
        # Reconstruct the quick filters with proper objects
        quick_filters = {}
        
        # Convert class_level pk back to object
        if quick_filters_raw.get('class_level'):
            try:
                from .models import ClassLevel
                quick_filters['class_level'] = ClassLevel.objects.get(pk=quick_filters_raw['class_level'])
            except ClassLevel.DoesNotExist:
                pass
        
        # Copy other simple fields
        if quick_filters_raw.get('time_needed'):
            quick_filters['time_needed'] = quick_filters_raw['time_needed']
        
        if quick_filters_raw.get('budget_band'):
            quick_filters['budget_band'] = quick_filters_raw['budget_band']
        
        # Use enhanced find_matches
        from .tlr_engine import find_matches
        suggestions = find_matches(quick_filters, keywords=keywords)
        
        context = {
            "suggestions": suggestions,
            "search_type": "keyword",
            "keywords": keywords,
            "result_count": len(suggestions)
        }
        
    else:
        # Handle route-based search results (existing logic)
        filters = request.session.get("filters")
        route = request.session.get("route")
        routes = request.session.get("routes", [])
        
        if not filters and not routes:
            return redirect("route_select")
        
        # Use enhanced engine for multiple routes
        from .tlr_engine import find_matches
        if routes:
            suggestions = find_matches(filters or {}, routes=routes)
        else:
            suggestions = find_matches(filters, routes=[route] if route else [])
        
        context = {
            "suggestions": suggestions,
            "search_type": "advanced",
            "routes": routes or [route],
            "result_count": len(suggestions)
        }
    
    # Add Pinterest boards logic (existing code)
    keywords = set()
    for tlr in context["suggestions"]:
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

    matched_boards = []
    stopwords = {"the", "and", "or", "for", "to", "in", "on", "of", "with", "by", "at", "a", "an", "from"}
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
    
    context["pinterest_boards"] = matched_boards
    return render(request, "results.html", context)



def get_visible_fields(routes):
    """Determine which form fields to show based on selected routes."""
    fields = set()

    for route in routes:
        if route == "curriculum":
            fields.update(['class_level', 'subject', 'term', 'strand', 'substrand', 'standard', 'indicator'])
        elif route == "key_area":
            fields.add('key_area')
        elif route == "competency":
            fields.add('competency')
        elif route == "theme":
            fields.add('theme')
        elif route == "resource":
            fields.add('resource_type')
        elif route == "goal":
            fields.add('goal')

    fields.update(['intended_use', 'time_needed', 'budget_band', 'bloom_level', 
                    'class_size', 'learning_styles', 'special_needs', 'materials_available'])

    return fields



def get_search_suggestions(keywords):
    """Use OpenAI to suggest better search terms for TLR discovery."""
    try:
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        prompt = f"""
        A teacher is searching for Teaching and Learning Resources (TLRs) using these keywords: "{keywords}"
        
        Suggest 3-5 alternative or related search terms that might help them find relevant educational resources for Ghana's early childhood curriculum (Creche to Class 3).
        
        Focus on:
        - Learning activities
        - Educational materials  
        - Teaching methods
        - Curriculum topics
        
        Return only the search terms, separated by commas.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.7
        )
        
        suggestions = response.choices[0].message.content.strip().split(',')
        return [s.strip() for s in suggestions[:5]]
        
    except Exception as e:
        print(f"OpenAI suggestion error: {e}")
        return []

def ajax_search_suggestions(request):
    keywords = request.GET.get('q', '')
    if len(keywords) > 3:
        suggestions = get_search_suggestions(keywords)
        return JsonResponse({'suggestions': suggestions})
    return JsonResponse({'suggestions': []})

def serialize_for_session(data):
    """Convert Django objects to JSON-serializable format for session storage."""
    serialized = {}
    for key, value in data.items():
        if isinstance(value, Model):
            serialized[key] = value.pk
        elif hasattr(value, "__iter__") and not isinstance(value, str):
            serialized[key] = [obj.pk if isinstance(obj, Model) else obj for obj in value]
        else:
            serialized[key] = value
    return serialized

def deserialize_from_session(data):
    """Convert session data back to Django objects."""
    # This would require knowing the model types, so the specific approach above is better
    pass

@method_decorator(login_required, name='dispatch')
class ActivityAPIView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            action = data.get('action')
            
            # Map client-side actions to our activity model actions
            action_mapping = {
                'page_view': 'page_view',
                'button_click': 'button_click',
                'form_submitted': 'form_submitted',
                'search_input': 'search',
                'session_end': 'session_end',
                'ajax_request': 'search',
                'ajax_error': 'error_encountered'
            }
            
            mapped_action = action_mapping.get(action, 'page_view')
            
            # Only save if it's a valid action
            if mapped_action:
                from .models import UserActivity
                from datetime import timedelta
                
                activity_data = {
                    'user': request.user,
                    'action': mapped_action,
                    'session_id': request.session.session_key,
                    'ip_address': self.get_client_ip(request),
                    'page_url': data.get('url', request.build_absolute_uri()),
                    'request_method': 'POST',
                }
                
                # Add specific data based on action
                if action == 'button_click':
                    activity_data['element_clicked'] = data.get('element', '')
                    activity_data['scroll_depth'] = data.get('scroll_depth')
                
                elif action == 'search_input':
                    activity_data['search_query'] = data.get('query', '')
                
                elif action == 'session_end':
                    time_on_page = data.get('time_on_page')
                    if time_on_page:
                        activity_data['time_on_page'] = timedelta(seconds=time_on_page)
                    activity_data['scroll_depth'] = data.get('max_scroll_depth')
                
                elif action == 'ajax_request':
                    activity_data['response_time'] = data.get('response_time', 0) / 1000  # Convert to seconds
                    activity_data['search_query'] = self.extract_search_from_url(data.get('url', ''))
                
                elif action == 'ajax_error':
                    activity_data['error_message'] = data.get('error', '')
                
                elif action == 'page_view':
                    activity_data['screen_resolution'] = data.get('screen_resolution', '')
                
                # Save the activity
                activity = UserActivity(**activity_data)
                activity._session_key = request.session.session_key
                activity.save()
            
            return JsonResponse({'status': 'success'})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def extract_search_from_url(self, url):
        """Extract search query from URL parameters"""
        try:
            from urllib.parse import urlparse, parse_qs
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            return params.get('q', [''])[0] or params.get('keywords', [''])[0]
        except:
            return ''

# Simple function-based view alternative
@login_required
@require_POST
def activity_api(request):
    try:
        data = json.loads(request.body)
        # Process and save activity data here
        # (You can use the same logic as in the class-based view above)
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)