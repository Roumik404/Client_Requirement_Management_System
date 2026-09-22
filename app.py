import re
from datetime import datetime

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

app = Flask(__name__)
app.secret_key = "client_requirement_secret"

USERNAME = "admin"
PASSWORD = "1234"

users = {
    USERNAME: {
        "password": PASSWORD,
        "email": "admin@clientreq.local"
    }
}

requests = []
EMAIL_LOGS = []

PRIORITIES = ["High", "Medium", "Low"]

STATUSES = [
    "New",
    "Under Review",
    "Requirement Clarification",
    "Approved",
    "Rejected",
    "Completed"
]

CATEGORIES = [
    "AI / Machine Learning",
    "Generative AI",
    "Automation",
    "Web Application",
    "Data Analytics",
    "Cloud / DevOps",
    "Other"
]


def login_required(view_func):
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)

    wrapper.__name__ = view_func.__name__
    return wrapper


# -----------------------------
# Solution Recommendation
# -----------------------------
def recommend_solution(data):

    text = (
        data["business_problem"] + " " +
        data["features"] + " " +
        data["technology"]
    ).lower()

    result = []

    if any(word in text for word in [
        "prediction", "classification", "forecast",
        "machine learning", "ml"
    ]):
        result.append("AI / Machine Learning")

    if any(word in text for word in [
        "chatbot", "generative ai", "gpt",
        "llm", "text generation"
    ]):
        result.append("Generative AI")

    if any(word in text for word in [
        "automation", "automate", "rpa", "workflow"
    ]):
        result.append("Automation")

    if any(word in text for word in [
        "website", "web application",
        "web app", "portal", "e-commerce"
    ]):
        result.append("Web Application")

    if any(word in text for word in [
        "analytics", "dashboard",
        "reporting", "data analysis"
    ]):
        result.append("Data Analytics")

    if any(word in text for word in [
        "cloud", "aws", "azure",
        "devops", "docker"
    ]):
        result.append("Cloud / DevOps")

    if not result:
        result.append("Other")

    return result


# -----------------------------
# Validation
# -----------------------------
def validate_request_form(data):

    required_fields = {
        "client_name": "client information",
        "contact_person": "client information",
        "email": "client information",
        "phone": "client information",
        "industry": "client information",
        "project_title": "project requirements",
        "business_problem": "project requirements",
        "expected_outcome": "project requirements",
        "features": "project requirements",
        "priority": "project requirements"
    }

    missing = [
        field for field in required_fields
        if not data.get(field, "").strip()
    ]

    if missing:
        section = required_fields[missing[0]]
        return f"Please fill in all required {section}."

    if not re.fullmatch(
        r"[^@\s]+@[^@\s]+\.[^@\s]+",
        data["email"]
    ):
        return "Please enter a valid email address."

    if (
        not data["phone"].isdigit()
        or len(data["phone"]) != 10
    ):
        return "Phone number must contain exactly 10 digits."

    if data["priority"] not in PRIORITIES:
        return "Please select a valid priority."

    return ""


# -----------------------------
# Landing Page
# -----------------------------
@app.route("/")
def landing():
    return render_template("landing.html")


# -----------------------------
# Login
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    error = ""

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username]["password"] == password:
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("dashboard"))

        else:
            error = "Invalid username or password."

    return render_template(
        "login.html",
        error=error
    )


# -----------------------------
# Account Registration
# -----------------------------
@app.route("/register", methods=["GET", "POST"])
def register():

    error = ""
    form_data = {}

    if request.method == "POST":
        form_data = {
            "username": request.form.get("username", "").strip(),
            "email": request.form.get("email", "").strip(),
            "password": request.form.get("password", ""),
            "confirm_password": request.form.get("confirm_password", "")
        }

        username = form_data["username"]

        if len(username) < 3:
            error = "Username must contain at least 3 characters."
        elif username in users:
            error = "That username is already in use."
        elif not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", form_data["email"]):
            error = "Please enter a valid email address."
        elif len(form_data["password"]) < 4:
            error = "Password must contain at least 4 characters."
        elif form_data["password"] != form_data["confirm_password"]:
            error = "Passwords do not match."
        else:
            users[username] = {
                "password": form_data["password"],
                "email": form_data["email"]
            }
            return redirect(url_for("login", registered="1"))

    return render_template(
        "register.html",
        error=error,
        form_data=form_data
    )


# -----------------------------
# Dashboard
# -----------------------------
@app.route("/dashboard")
@login_required
def dashboard():

    total = len(requests)

    new = sum(
        1 for r in requests
        if r["status"] == "New"
    )

    review = sum(
        1 for r in requests
        if r["status"] == "Under Review"
    )

    approved = sum(
        1 for r in requests
        if r["status"] == "Approved"
    )

    high = sum(
        1 for r in requests
        if r["priority"] == "High"
    )

    completed = sum(
        1 for r in requests
        if r["status"] == "Completed"
    )

    active = total - completed
    completion_rate = round((completed / total) * 100) if total else 0
    review_rate = round((review / total) * 100) if total else 0
    priority_rate = round((high / total) * 100) if total else 0
    approval_rate = round((approved / total) * 100) if total else 0

    categories = {
        "AI / Machine Learning": 0,
        "Generative AI": 0,
        "Automation": 0,
        "Web Application": 0,
        "Data Analytics": 0,
        "Cloud / DevOps": 0,
        "Other": 0
    }

    industries = {}

    for r in requests:

        for category in r["recommendation"]:
            categories[category] += 1

        industry = r["industry"]

        if industry in industries:
            industries[industry] += 1
        else:
            industries[industry] = 1

    return render_template(
        "dashboard.html",
        total=total,
        new=new,
        review=review,
        approved=approved,
        high=high,
        completed=completed,
        active=active,
        completion_rate=completion_rate,
        review_rate=review_rate,
        priority_rate=priority_rate,
        approval_rate=approval_rate,
        recent_requests=list(reversed(requests[-4:])),
        category_counts=categories,
        industry_counts=industries
    )


# -----------------------------
# New Request
# -----------------------------
@app.route("/new-request", methods=["GET", "POST"])
@login_required
def new_request():

    error = ""
    form_data = {}

    if request.method == "POST":

        form_data = {
            key: request.form.get(
                key, ""
            ).strip()
            for key in [
                "client_name",
                "contact_person",
                "email",
                "phone",
                "industry",
                "project_title",
                "business_problem",
                "current_process",
                "expected_outcome",
                "features",
                "technology",
                "priority",
                "additional_requirements"
            ]
        }

        error = validate_request_form(form_data)

        if not error:

            new_req = {

                "id": f"REQ-{len(requests) + 1:03d}",

                **form_data,

                "status": "New",
                "comments": "",

                "notification": "",

                "last_updated": datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                )
            }

            new_req["recommendation"] = recommend_solution(
                new_req
            )

            requests.append(new_req)

            return redirect(
                url_for("dashboard")
            )

    return render_template(
        "req_form.html",
        error=error,
        form_data=form_data
    )


# -----------------------------
# View All Requests
# -----------------------------
@app.route("/requests")
@login_required
def view_requests():

    search = request.args.get(
        "search", ""
    ).lower()

    industry = request.args.get(
        "industry", ""
    )

    category = request.args.get(
        "category", ""
    )

    status = request.args.get(
        "status", ""
    )

    filtered = []

    for r in requests:

        if search:

            if (
                search not in r["client_name"].lower()
                and search not in r["project_title"].lower()
            ):
                continue

        if industry and r["industry"] != industry:
            continue

        if category and category not in r["recommendation"]:
            continue

        if status and r["status"] != status:
            continue

        filtered.append(r)

    industries = sorted(
        set(r["industry"] for r in requests)
    )

    return render_template(
        "requests.html",
        requests=filtered,
        industries=industries,
        categories=CATEGORIES,
        search=search,
        selected_industry=industry,
        selected_category=category,
        selected_status=status
    )


# -----------------------------
# Request Details
# -----------------------------
@app.route(
    "/request/<request_id>",
    methods=["GET", "POST"]
)
@login_required
def request_detail(request_id):

    req = next(
        (
            r for r in requests
            if r["id"] == request_id
        ),
        None
    )

    if req is None:
        return "Request not found", 404

    error = ""

    if request.method == "POST":

        status = request.form.get(
            "status", ""
        )

        priority = request.form.get(
            "priority", ""
        )

        comments = request.form.get(
            "comments", ""
        ).strip()

        if status not in STATUSES:
            error = (
                "Please select a valid status."
            )

        elif priority not in PRIORITIES:
            error = (
                "Please select a valid priority."
            )

        else:

            req["status"] = status
            req["priority"] = priority
            req["comments"] = comments

            req["notification"] = (
                f"Client '{req['client_name']}' "
                f"has been notified that "
                f"Request {req['id']} "
                f"has been updated."
            )

            req["last_updated"] = (
                datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                )
            )

            EMAIL_LOGS.append({
                "request_id": req["id"],
                "email": req["email"],
                "subject": "Project Request Update",
                "message":
                    f"Hello "
                    f"{req['contact_person']}, "
                    f"your request "
                    f"'{req['project_title']}' "
                    f"has been updated. "
                    f"Status: {status}, "
                    f"Priority: {priority}"
            })

            flash(
                f"Request {req['id']} "
                f"updated successfully. "
                f"Client notification sent.",
                "success"
            )

            return redirect(
                url_for(
                    "request_detail",
                    request_id=request_id
                )
            )

    return render_template(
        "req_details.html",
        req=req,
        error=error
    )


# -----------------------------
# Logout
# -----------------------------
@app.route("/logout", methods=["POST", "GET"])
def logout():

    session.clear()

    return redirect(url_for("landing"))
    


# -----------------------------
# Run Application
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)