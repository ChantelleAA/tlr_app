# TLR Helper

**TLR Helper** is a Django web application that helps teachers find and use effective Teaching and Learning Resources (TLRs) that are aligned with Ghana’s Standards-Based Curriculum (SBC). It guides users through curriculum-based filtering to suggest resources appropriate for the class level, subject, and learning goals. The app also includes tools for filtering based on learning styles and special needs, making it more inclusive.

---

## Project Overview

This tool is designed to support teachers and curriculum developers with:

- Suggestions for teaching aids based on curriculum structure.
- Class-specific resource filtering from Crèche to Class 3.
- A database of materials including themes, competencies, and learning areas.
- PDF download support for offline use.
- Support for different learner needs including special education filters.
- A foundation for integrating visual idea search from platforms like Pinterest.

---

## Preview

Below is a demonstration of how the TLR Helper works:

![TLR Helper Demo](https://github.com/ChantelleAA/tlr_app/blob/clearer_searches/tlr_helper.gif)

---

## Features

- Curriculum-based resource search: Class Level → Subject → Strand → Sub-strand
- Preloaded data from the official Ghana SBC
- Downloadable TLRs in PDF format
- Smart filters using HTMX for dynamic field updates
- Options to filter by:
  - Time needed
  - Budget range
  - Intended use (e.g., introduction, teaching aid, assessment)
  - Bloom’s Taxonomy levels
  - Learning styles
  - Special education needs
- Basic tracking of TLR download counts and usage outcomes

---

## Setup Instructions

### Requirements

- Python 3.11+
- PostgreSQL (or SQLite for development)
- Django 5.x

### 1. Clone the Repository

```bash
git clone https://github.com/ChantelleAA/tlr_app.git
cd tlr_app
````

### 2. Set Up Environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Create Environment Variables

Set up a `.env` file or environment variables with the following:

```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=your-postgres-url
```

For SQLite in local development, adjust `DATABASES` in `settings.py` accordingly.

### 4. Apply Migrations and Load Initial Data

```bash
python manage.py migrate
python manage.py load_fixtures_safe
```

The `load_fixtures_safe` command avoids errors from duplicate entries and only inserts what's missing or updates existing ones.

### 5. Run the Application

```bash
python manage.py runserver
```

---

## Deployment Notes (Render or VPS)

Make sure the following script is used in your startup (`start.sh`):

```bash
#!/bin/bash

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Loading initial fixture data..."
python manage.py load_fixtures_safe || echo "Fixture load skipped (error or already loaded)"

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
gunicorn core.wsgi:application
```

This ensures the application doesn’t crash if fixtures already exist.

---

## File Structure

```
tlr_helper/
├── suggestor/              # Main app for TLR logic
│   ├── fixtures/           # Preloaded curriculum-aligned data
│   ├── management/
│   │   └── commands/
│   │       └── load_fixtures_safe.py  # Custom loader with conflict resolution
├── templates/
├── static/
├── start.sh
├── requirements.txt
```

---

## Data Source

All curriculum data is based on the official Ghana Standards-Based Curriculum (NaCCA, 2019), including strands, sub-strands, learning indicators, and goals.

---

## Future Plans

* Integration with Pinterest or Google Image Search for visual inspiration.
* Admin dashboard for uploading and managing custom TLRs.
* AI-based suggestions based on teacher preferences or past usage.
* Export to offline formats and mobile-optimized versions.

---

## Author

Built and maintained by [ChantelleAA](https://github.com/ChantelleAA), as part of work with TEDD Ghana and AIMS.

---

## License

This project is licensed under the MIT License.


