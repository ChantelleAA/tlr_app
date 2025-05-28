Below is a step-by-step roadmap that keeps everything in Python, avoids heavy JavaScript, and lets you grow the project gradually from a working prototype to a richer app.

PHASE 1 · Prepare your data

* Create a spreadsheet (or CSV) with one row per ready-made TLR.
  Columns: strand, sub\_strand, class\_level, intended\_use, tlr\_type, title, brief\_description, materials, time\_needed, accessibility\_notes, classroom\_setup, steps\_to\_make, tips\_for\_use.
* Save it in data/tlr\_library.csv.

PHASE 2 · Set up the project skeleton

```
tlr_helper/
│
├─ app/
│   ├─ main.py          # Flask entry point
│   ├─ models.py        # SQLAlchemy models
│   ├─ db.py            # DB helpers
│   ├─ tlr_engine.py    # suggestion logic
│   ├─ templates/
│   │     ├─ base.html
│   │     ├─ index.html
│   │     └─ results.html
│   └─ static/
│
├─ data/
│   └─ tlr_library.csv
└─ requirements.txt
```

requirements.txt

```
flask
flask_sqlalchemy
pandas
sentence-transformers      # optional fallback generator
openai                     # if you decide to use GPT
```

PHASE 3 · Load the library into a tiny database

* In models.py define a `Tlr` model with the columns above.
* Write a one-off script (or a function in db.py) that reads `tlr_library.csv` with pandas and bulk-inserts rows into SQLite.

PHASE 4 · Build the suggestion engine (tlr\_engine.py)

1. `find_matches(inputs) → List[Tlr]`
   • Filter by strand, class\_level, intended\_use.
   • Further filter by materials, learner\_type, classroom\_setup if the teacher supplied them.
   • Rank by time\_fit and preferred\_format.
2. If the list is empty, call `fallback_generate(inputs)`.
   • A quick baseline: concatenate the inputs into a prompt like
   *“Suggest two practical TLR ideas for …”* and send to OpenAI (or a local SentenceTransformer and some rule-based text).
   • Wrap the response into the same Tlr shape (you do not have to store it permanently unless you wish).

PHASE 5 · Create the Flask views

* **index route**: renders index.html with a form containing:
  • strand (text with datalist)
  • sub-strand (optional text)
  • class level (select)
  • intended use (select)
  • materials (multi-select checkboxes)
  • learning outcome (textarea, optional)
  • learner type (multi-select)
  • time available (radio buttons)
  • preferred format (multi-select)
  • classroom setup (multi-select)
* **/suggest route (POST)**:
  • collect form data, call `find_matches`, then render results.html.
  • show each suggestion in a card: title, description, materials, time, steps, usage tips, and a “Download as .txt” link that simply returns a text file built on-the-fly from those fields.

PHASE 6 · Simple HTML with Jinja, zero JavaScript

* base.html: Bootstrap CDN + a small CSS file.
* index.html: extend base, include the form.
* results.html: loop over suggestions and display cards.
  If you later want a slicker UI, you can replace Bootstrap with Tailwind and sprinkle HTMX or Alpine.js for interactivity, still without leaving Python for heavy React work.

PHASE 7 · Testing

* Write pytest tests for `find_matches` to be sure your filters work.
* Add a tiny Selenium script (optional) to smoke-test the form end-to-end.

PHASE 8 · Packaging & deployment

* Add a `run.sh` that sets `FLASK_APP=app.main` and `flask run`.
* Push to GitHub.
* Deploy on Render, Railway, Fly.io, or a small VPS. A free SQLite database is enough to start.

PHASE 9 · Iterate

* When teachers start using it, note missing strands or TLR ideas and extend `tlr_library.csv`.
* Add an admin view (Flask-Login + a simple form) to create or edit TLRs through the browser.
* Cache AI-generated suggestions back into the database so the next teacher gets them instantly.

Key points for a Python-first developer

* The whole stack is Flask + Jinja + SQLite: no heavy front-end build tools required.
* You can defer all AI work. A pure rules-based filter already delivers value if the CSV is rich.
* Each new feature (PDF download, user accounts, analytics) is an independent Flask blueprint you can add later.

Start by filling the CSV with twenty well-tagged TLRs and wiring up `find_matches`. After you see cards appearing in the browser, everything else is refinement.
