from flask import Flask, render_template, request, redirect, send_file
from PIL import Image
import pytesseract
import os
from form_filler import fill_event_form
from security import save_profile, load_profile


app = Flask(__name__)
app.secret_key = "smart-form-fill-secret"

UPLOAD_FOLDER = "uploads"
FILLED_FOLDER = "filled_forms"
PROFILE_FILE = "profile.json"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(FILLED_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html", profile=load_profile())


@app.route("/save-profile", methods=["POST"])
def save_profile_route():

    profile = {
        "full_name": request.form.get("full_name", ""),
        "dob": request.form.get("dob", ""),
        "gender": request.form.get("gender", ""),
        "phone": request.form.get("phone", ""),
        "email": request.form.get("email", ""),
        "address": request.form.get("address", "")
    }

    save_profile(profile)

    return redirect("/")


@app.route("/upload", methods=["POST"])
def upload():

    file = request.files.get("file")

    if not file:
        return "No file uploaded", 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    image = Image.open(filepath)

    text = pytesseract.image_to_string(image)

    profile = load_profile()

    # This form needs these additional details
    required = [
        "full_name",
        "dob",
        "gender",
        "phone",
        "email",
        "source",
        "tickets",
        "payment",
        "agreement",
        "date_signed"
    ]

    missing = []

    for field in required:
        if not profile.get(field):
            missing.append(field)

    if missing:

        return render_template(
            "questions.html",
            fields=missing,
            filename=file.filename
        )

    return create_filled_form(file.filename, profile)


@app.route("/answer-questions", methods=["POST"])
def answer_questions():

    profile = load_profile()

    for key, value in request.form.items():

        if value.strip():
            profile[key] = value.strip()

    save_profile(profile)

    filename = request.form.get("filename")

    return create_filled_form(filename, profile)


def create_filled_form(filename, data):

    input_path = os.path.join(UPLOAD_FOLDER, filename)

    output_filename = "filled_" + filename
    output_path = os.path.join(
        FILLED_FOLDER,
        output_filename
    )

    fill_event_form(
        input_path,
        output_path,
        data
    )

    return render_template(
        "filled.html",
        filename=output_filename
    )


@app.route("/download/<filename>")
def download(filename):

    path = os.path.join(
        FILLED_FOLDER,
        filename
    )

    return send_file(
        path,
        as_attachment=True
    )

@app.route("/filled_forms/<filename>")
def filled_image(filename):

    path = os.path.join(FILLED_FOLDER, filename)

    return send_file(path)

if __name__ == "__main__":
    app.run(debug=True)