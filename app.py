from flask import Flask, render_template, request

app = Flask(__name__)

ALLOWED_DEGREES = ["Bachelor in CS", "Masters in CS", "Bachelor and Masters in CS", "None"]
ALLOWED_CERTS = ["PMI Lean Project Management Certification", "None"]

POSITIONS = [
    {
        "title": "Entry-Level Python Engineer",
        "needed": [
            {
                "check": lambda a: a["python_coursework"],
                "fail": "Python course work not completed",
            },
            {
                "check": lambda a: a["software_eng_coursework"],
                "fail": "Software Engineering course work not completed",
            },
            {
                "check": lambda a: has_degree(a["degree"], "bachelor"),
                "fail": "Required qualification is Bachelor in CS",
            },
        ],
        "desired": [
            {
                "text": "Agile course",
                "check": lambda a: a["agile_course"],
            }
        ],
    },
    {
        "title": "Python Engineer",
        "needed": [
            {
                "check": lambda a: a["python_years"] >= 3,
                "fail": "Needs at least 3 years of Python development",
            },
            {
                "check": lambda a: a["data_dev_years"] >= 1,
                "fail": "Needs at least 1 year of data development",
            },
            {
                "check": lambda a: a["agile_project_years"] >= 1,
                "fail": "Needs Agile project experience (at least 1 year)",
            },
            {
                "check": lambda a: has_degree(a["degree"], "bachelor"),
                "fail": "Required qualification is Bachelor in CS",
            },
        ],
        "desired": [
            {
                "text": "Used Git",
                "check": lambda a: a["used_git"],
            }
        ],
    },
    {
        "title": "Project Manager",
        "needed": [
            {
                "check": lambda a: a["manage_years"] >= 3,
                "fail": "Needs at least 3 years managing software projects",
            },
            {
                "check": lambda a: a["agile_project_years"] >= 2,
                "fail": "Needs at least 2 years of Agile project experience",
            },
            {
                "check": lambda a: a["certification"] == "PMI Lean Project Management Certification",
                "fail": "Required qualification is PMI Lean Project Management Certification",
            },
        ],
        "desired": [],
    },
    {
        "title": "Senior Knowledge Engineer",
        "needed": [
            {
                "check": lambda a: a["python_years"] >= 4,
                "fail": "Needs at least 4 years of Python development",
            },
            {
                "check": lambda a: a["expert_system_years"] >= 2,
                "fail": "Needs at least 2 years developing Expert Systems",
            },
            {
                "check": lambda a: a["data_arch_years"] >= 2,
                "fail": "Needs at least 2 years in data architecture and data development",
            },
            {
                "check": lambda a: has_degree(a["degree"], "masters"),
                "fail": "Required qualification is Masters in CS",
            },
        ],
        "desired": [],
    },
]


def has_degree(degree_value, needed):
    if needed == "bachelor":
        return degree_value in ("Bachelor in CS", "Bachelor and Masters in CS")
    if needed == "masters":
        return degree_value in ("Masters in CS", "Bachelor and Masters in CS")
    return False


def parse_int(form, key):
    value = form.get(key, "").strip()
    if value == "":
        return None
    try:
        parsed = int(value)
    except ValueError:
        return None
    return parsed


def validate(applicant):
    errors = []

    if applicant["degree"] not in ALLOWED_DEGREES:
        errors.append(
            f'Invalid degree value: "{applicant["degree"] or "(empty)"}". '
            f'Use exactly one of: {", ".join(ALLOWED_DEGREES)}.'
        )

    if applicant["certification"] not in ALLOWED_CERTS:
        errors.append(
            f'Invalid certification value: "{applicant["certification"] or "(empty)"}". '
            f'Use exactly one of: {", ".join(ALLOWED_CERTS)}.'
        )

    year_fields = [
        ("Years of Python development", "python_years"),
        ("Years of data development", "data_dev_years"),
        ("Years of Agile project experience", "agile_project_years"),
        ("Years managing software projects", "manage_years"),
        ("Years developing Expert Systems", "expert_system_years"),
        ("Years in data architecture and data development", "data_arch_years"),
    ]

    for label, key in year_fields:
        value = applicant[key]
        if value is None or value < 0 or value > 100:
            errors.append(f"{label} must be a whole number from 0 to 100.")

    return errors


def evaluate(applicant):
    qualified = []
    not_qualified = []

    for position in POSITIONS:
        unmet = [r["fail"] for r in position["needed"] if not r["check"](applicant)]
        met_desired = [d["text"] for d in position["desired"] if d["check"](applicant)]
        unmet_desired = [d["text"] for d in position["desired"] if not d["check"](applicant)]

        entry = {
            "title": position["title"],
            "unmet": unmet,
            "met_desired": met_desired,
            "unmet_desired": unmet_desired,
        }

        if unmet:
            not_qualified.append(entry)
        else:
            qualified.append(entry)

    return qualified, not_qualified


@app.route("/", methods=["GET", "POST"])
def index():
    errors = []
    qualified = []
    not_qualified = []

    form_data = {
        "degree": "",
        "certification": "",
        "python_years": "",
        "data_dev_years": "",
        "agile_project_years": "",
        "manage_years": "",
        "expert_system_years": "",
        "data_arch_years": "",
        "python_coursework": False,
        "software_eng_coursework": False,
        "agile_course": False,
        "used_git": False,
    }

    if request.method == "POST":
        form_data = {
            "degree": request.form.get("degree", "").strip(),
            "certification": request.form.get("certification", "").strip(),
            "python_years": request.form.get("python_years", "").strip(),
            "data_dev_years": request.form.get("data_dev_years", "").strip(),
            "agile_project_years": request.form.get("agile_project_years", "").strip(),
            "manage_years": request.form.get("manage_years", "").strip(),
            "expert_system_years": request.form.get("expert_system_years", "").strip(),
            "data_arch_years": request.form.get("data_arch_years", "").strip(),
            "python_coursework": request.form.get("python_coursework") == "on",
            "software_eng_coursework": request.form.get("software_eng_coursework") == "on",
            "agile_course": request.form.get("agile_course") == "on",
            "used_git": request.form.get("used_git") == "on",
        }

        applicant = {
            "degree": form_data["degree"],
            "certification": form_data["certification"],
            "python_years": parse_int(request.form, "python_years"),
            "data_dev_years": parse_int(request.form, "data_dev_years"),
            "agile_project_years": parse_int(request.form, "agile_project_years"),
            "manage_years": parse_int(request.form, "manage_years"),
            "expert_system_years": parse_int(request.form, "expert_system_years"),
            "data_arch_years": parse_int(request.form, "data_arch_years"),
            "python_coursework": form_data["python_coursework"],
            "software_eng_coursework": form_data["software_eng_coursework"],
            "agile_course": form_data["agile_course"],
            "used_git": form_data["used_git"],
        }

        errors = validate(applicant)
        if not errors:
            qualified, not_qualified = evaluate(applicant)

    return render_template(
        "index.html",
        errors=errors,
        qualified=qualified,
        not_qualified=not_qualified,
        form_data=form_data,
        allowed_degrees=ALLOWED_DEGREES,
        allowed_certs=ALLOWED_CERTS,
    )


if __name__ == "__main__":
    app.run(debug=True)
