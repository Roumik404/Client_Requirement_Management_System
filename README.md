# ClientReq

A Flask-based client project requirement and request management system. It captures client needs, recommends solution categories with simple keyword rules, and supports request review workflows through a polished light/dark themed workspace.

## Requirements

- Python 3.10+
- Flask

## Run Locally

From the project directory:

```powershell
.\venv\Scripts\Activate.ps1
python app.py
```

Open `http://127.0.0.1:5000` in a browser.

If the virtual environment has not been created yet:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install Flask
```

## Authentication

The application includes a default demo account:

- Username: `admin`
- Password: `1234`

New users can select **Create an account** from the login page. Registration validates the username, email address, password length, password confirmation, and duplicate usernames.

User accounts are stored in memory for this demo, so newly registered accounts reset when the application restarts. Password visibility can be toggled with the eye icon on login and registration forms.

## Workflow

1. Open the landing page and select **Open workspace** or **Sign in**.
2. Sign in with the demo account or create a new account.
3. Review live dashboard metrics, completion/review/priority rates, request-flow bars, and recent activity.
4. Create a request with client and project requirement information.
5. The system generates a request ID and recommends one or more solution categories.
6. Search or filter requests by client/project, industry, category, or status.
7. Open a request to review its details, update status and priority, and add reviewer comments.

Requests are stored in an in-memory Python list and reset when the application restarts.

## User Interface

- Product-focused landing page with dashboard preview and capability highlights.
- Responsive dashboard with graphical request-flow data and compact rate cards.
- Professional request list, request detail, and intake form layouts.
- Light and dark themes with the selected theme saved in browser local storage.
- Responsive navigation for desktop, tablet, and mobile screens.

## Solution-Category Rules

The recommendation function checks the combined business problem, required features, and preferred technology text. Matching is case-insensitive and can produce multiple categories:

- **AI / Machine Learning:** `prediction`, `classification`, `forecast`, `machine learning`, or `ml`
- **Generative AI:** `chatbot`, `generative ai`, `gpt`, `llm`, or `text generation`
- **Automation:** `automation`, `automate`, `rpa`, or `workflow`
- **Web Application:** `website`, `web application`, `web app`, `portal`, or `e-commerce`
- **Data Analytics:** `analytics`, `dashboard`, `reporting`, or `data analysis`
- **Cloud / DevOps:** `cloud`, `aws`, `azure`, `devops`, or `docker`
- **Other:** used when no category keyword matches

## Validation

The server validates required client and project fields, basic email format, exactly ten numeric phone digits, and allowed priority/status values. Invalid submissions return a clear error without crashing, and entered form values are preserved.

## Project Structure

```text
client_requirement_app/
├── app.py
├── README.md
├── static/
│   ├── app.js
│   └── style.css
└── templates/
    ├── base.html
    ├── dashboard.html
    ├── landing.html
    ├── login.html
    ├── req_details.html
    ├── req_form.html
    ├── register.html
    └── requests.html
```

## Routes

| Route | Purpose |
| --- | --- |
| `/` | Public landing page |
| `/login` | Sign in |
| `/register` | Create an account |
| `/dashboard` | Live operational dashboard |
| `/new-request` | Create a project request |
| `/requests` | Search and filter requests |
| `/request/<request_id>` | View and update a request |
