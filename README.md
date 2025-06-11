# TLR Helper – Teaching and Learning Resource Generator for Early Childhood Education

**TLR Helper** is a Django-based web application designed to help Ghanaian teachers (Creche to Class 3) search, filter, and download effective Teaching and Learning Resources (TLRs) aligned with the Standards-Based Curriculum. The app supports both guided and exploratory discovery of materials using curriculum metadata, learning tags, and intelligent search features.

---

## 🌟 Key Features

- **Search by Curriculum Structure**  
  Find TLRs based on class level, subject, term, strand, sub-strand, content standard, and indicator.

- **Explore by Learning Tags**  
  Filter TLRs using themes, key learning areas, core competencies, resource types, goal tags, and more.

- **Keyword-Based Discovery**  
  Enter keywords like "counting game", "body parts", or "literacy visuals" to match relevant TLRs across fields.

- **Intelligent Filtering**  
  Apply filters like intended use, time needed, budget range, class size, Bloom’s level, special needs, and learning styles.

- **Download & Print PDFs**  
  Each TLR can be downloaded as a well-formatted PDF, including materials list, classroom tips, and instructions.

- **OpenAI-Powered Suggestions**  
  Enhance your search experience with AI-generated keyword alternatives based on your input.

- **User Authentication**  
  Supports user login, signup, and role-based access to features like download tracking and personalized TLR creation.

- **Responsive UI with AJAX**  
  Dropdowns dynamically update based on previous choices (e.g., Class → Subject → Strand) for a smooth user flow.

---

## 🚀 Quickstart

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/tlr-helper.git
cd tlr-helper
```

### 2. Install Dependencies
Create a virtual environment and install required packages:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run Locally
```bash
python manage.py migrate
python manage.py runserver
```

### 4. Create a Superuser
```bash
python manage.py createsuperuser
```

---

## 🌐 Deployment (Render-ready)

This app is ready for deployment on [Render](https://render.com/). It includes:

- A `start.sh` script to:
  - Apply migrations
  - Load fixture data if missing
  - Create a default admin user (`chantelle/2241`)
  - Run health checks
  - Launch Gunicorn

To deploy:
- Add environment variable `RENDER=1`
- Set `PORT`, `ADMIN_USERNAME`, `ADMIN_PASSWORD`, and `ADMIN_EMAIL` as needed

---

## 📁 Project Structure

| File/Folder         | Purpose                                      |
|---------------------|----------------------------------------------|
| `models.py`         | Curriculum, TLR, tag, and relationship models |
| `forms.py`          | Forms for filtering, signup, contact         |
| `views.py`          | Main logic for routing, search, and PDF generation |
| `tlr_engine.py`     | Advanced matching, ranking, and filtering logic |
| `templates/`        | HTML templates for UI                        |
| `static/`           | Static files (CSS, JS, images)               |
| `start.sh`          | Deployment script for Render                 |
| `requirements.txt`  | Dependencies                                 |
| `settings.py`       | Project configuration                        |
| `urls.py`           | URL routes                                   |

---

## ✍️ Fixtures & Initial Data

On first run, the app can auto-populate:

- Class Levels (Creche to Class 3)
- Subjects per level
- Themes, Key Learning Areas, Competencies
- Goal tags, Resource types
- Learning styles and Special needs tags

This ensures users can start creating or searching TLRs without manual setup.

---

## 🧠 Example Use Case

A KG2 teacher needs a low-budget activity to reinforce "counting to 10" for a mixed-ability class.

1. They select:
   - Class: KG2
   - Subject: Numeracy
   - Strand: Numbers
   - Intended use: Reinforcement
   - Budget: ₵1–₵10
   - Special needs: Dyslexia
2. They get 3 matching TLRs, one of which is a **Counting Bottle Cap Game**.
3. They download the PDF and prepare it for the next day.

---

## 📬 Contact & Support

- Submit feedback or questions on the [Contact Page](https://tlr.teddghana.com/contact)
- Or email: `support@nileedge.com`, `teddghana@gmail.com`

---

## 🔐 Admin Credentials (Default)

- Username: `chantelle`
- Password: `2241`

---

## 📌 Notes

- This app supports PDF generation via `reportlab` and static HTML print views.
- Designed for early-grade resource creators, curriculum coordinators, and educational NGOs.
- Works with PostgreSQL (production) and SQLite (development).

---

## 📄 License

This project is licensed for educational and non-commercial use under TEDD Ghana. Contact the team for reuse or adaptation requests.

---