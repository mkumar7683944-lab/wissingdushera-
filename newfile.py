
from flask import Flask, request, jsonify, render_template_string
from werkzeug.utils import secure_filename
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport"
          content="width=device-width, initial-scale=1">
    <title>Happy Dussehra</title>
    <style>
        body {
            margin: 0;
            padding: 20px;
            text-align: center;
            font-family: Arial, sans-serif;
            background: linear-gradient(
                135deg, #8b0000, #ff9800, #ffd54f);
            color: white;
        }
        .card {
            max-width: 400px;
            margin: 20px auto;
            padding: 22px;
            border-radius: 20px;
            background: #fff8e1;
            color: #8b0000;
            box-shadow: 0 5px 20px #4a160055;
        }
        input, button {
            box-sizing: border-box;
            width: 100%;
            margin: 8px 0;
            padding: 12px;
            border-radius: 8px;
        }
        button {
            border: none;
            background: #b71c1c;
            color: white;
            font-size: 16px;
        }
        .photo {
            width: 150px;
            height: 150px;
            object-fit: cover;
            border-radius: 50%;
            border: 4px solid #ff9800;
        }
        h1 { color: #b71c1c; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🏹 Dussehra Greeting Maker 🪔</h2>

        <form method="POST" enctype="multipart/form-data">
            <input type="text" name="name"
                   placeholder="Enter your name" required>

            <input type="file" name="photo"
                   accept="image/png,image/jpeg,image/webp"
                   required>

            <button type="submit">Create Greeting</button>
        </form>

        {% if name and photo_url %}
            <hr>
            <img class="photo" src="{{ photo_url }}"
                 alt="User photo">
            <h1>Happy Dussehra, {{ name }}! 🎉</h1>
            <p>May victory, happiness and success
               always be with you.</p>
            <p>🪔 शुभ दशहरा 🪔</p>
        {% endif %}
    </div>
</body>
</html>
"""

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )

@app.route("/", methods=["GET", "POST"])
def home():
    name = ""
    photo_url = ""

    if request.method == "POST":
        name = request.form.get("name", "").strip()[:60]
        photo = request.files.get("photo")

        if not name:
            return "Please enter a name.", 400

        if not photo or not photo.filename:
            return "Please select a photo.", 400

        if not allowed_file(photo.filename):
            return "Use a PNG, JPG, JPEG or WEBP photo.", 400

        extension = secure_filename(
            photo.filename
        ).rsplit(".", 1)[1].lower()

        filename = uuid.uuid4().hex + "." + extension
        photo.save(os.path.join(UPLOAD_FOLDER, filename))
        photo_url = "/uploads/" + filename

    return render_template_string(
        HTML, name=name, photo_url=photo_url
    )

@app.route("/uploads/<path:filename>")
def uploaded_photo(filename):
    from flask import send_from_directory
    return send_from_directory(
        app.config["UPLOAD_FOLDER"], filename
    )

@app.route("/api/greeting")
def greeting_api():
    name = request.args.get("name", "Friend").strip()[:60]
    if not name:
        name = "Friend"

    return jsonify({
        "success": True,
        "festival": "Dussehra",
        "name": name,
        "message": f"Happy Dussehra, {name}!",
        "wish": "May victory, happiness and success be with you."
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
