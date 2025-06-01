# tlr_app
# TLR Helper

## Project Overview

TLR Helper is a Django-based web application designed to support teachers in creating effective Teaching and Learning Resources (TLRs). The application leverages Ghana's Standards-Based Curriculum (SBC) structure, facilitating educators' access to tailored resources aligned with specific curriculum components such as Class Levels, Subjects, Strands, Sub-strands, Themes, Key Learning Areas, and Core Competencies.

## Features

### Core Functionalities

* **Chained Dropdown Filters:** Easily filter TLRs by class level, subject, strand, and sub-strand.
* **Resource Recommendations:** Provides curated resources based on the user's specified educational parameters.
* **Curriculum Alignment:** Reflects accurate and detailed Ghana SBC curriculum structures.

### Enhanced Usability

* **Dynamic Filtering:** Utilizes HTMX for seamless, responsive interactions.
* **User-Friendly Interface:** Bootstrap-powered UI ensuring an intuitive user experience.

## Technical Stack

* **Framework:** Django 5.2
* **Frontend:** HTML, Bootstrap 5, HTMX
* **Database:** PostgreSQL

## Installation

Follow these steps to set up TLR Helper locally:

### Prerequisites

* Python 3.11 or higher
* PostgreSQL

### Steps

1. **Clone the Repository:**

   ```sh
   git clone <repository-url>
   cd tlr_helper
   ```

2. **Create Virtual Environment:**

   ```sh
   python -m venv env
   source env/bin/activate  # On Windows: .\env\Scripts\activate
   ```

3. **Install Dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Configure Database:**

   * Create PostgreSQL database and user

   ```sql
   CREATE DATABASE tlr_db;
   CREATE USER tlr_db_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE tlr_db TO tlr_db_user;
   ```

5. **Set Up Environment Variables:**
   Create `.env` file:

   ```sh
   DATABASE_URL=postgres://tlr_db_user:your_password@localhost:5432/tlr_db
   ```

6. **Apply Migrations:**

   ```sh
   python manage.py migrate
   ```

7. **Load Initial Data (Fixtures):**

   ```sh
   python manage.py loaddata fixtures.json
   ```

8. **Run Server:**

   ```sh
   python manage.py runserver
   ```

## Usage

Access the application via:

* Localhost: `http://127.0.0.1:8000/`

Navigate through chained dropdowns to select class levels, subjects, and curriculum components for personalized resource recommendations.

## Project Structure

```
tl_helper/
├── core/
│   ├── settings.py
│   └── urls.py
├── suggestor/
│   ├── models.py
│   ├── views.py
│   ├── templates/
│   ├── static/
│   └── fixtures.json
├── manage.py
├── requirements.txt
└── README.md
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support

For questions or issues, please open an issue in the repository or contact the project maintainer directly.
