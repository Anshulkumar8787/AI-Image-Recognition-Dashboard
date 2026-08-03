from flask import Flask, render_template, request, send_from_directory, send_file, redirect
import os
import csv
from datetime import datetime
from werkzeug.utils import redirect, secure_filename
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from model import predict_image

app = Flask(__name__)

# Upload Folder
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Allowed Extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# Create uploads folder
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

# History Folder
HISTORY_FOLDER = "history"
HISTORY_FILE = os.path.join(HISTORY_FOLDER, "history.csv")

os.makedirs(HISTORY_FOLDER, exist_ok=True)

def save_history(image_name, prediction):

    current_time = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")

    with open(HISTORY_FILE, "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            image_name,
            prediction["category"],
            prediction["detail"],
            prediction["confidence"],
            current_time
        ])
        
def load_history():

    history = []

    if os.path.exists(HISTORY_FILE):

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            history = list(reader)

    history.reverse()

    return history


# Report Folder   
REPORT_FOLDER = "reports"
os.makedirs(REPORT_FOLDER, exist_ok=True)

latest_prediction = None
latest_image = ""


@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None
    warning = ""
    image_filename = ""

    if request.method == "POST":

        # No file uploaded
        if "image" not in request.files:

            warning = "⚠ Please upload an image first."

            return render_template(
                "index.html",
                warning=warning,
                prediction=None,
                image_path=""
            )

        file = request.files["image"]

        # Empty file
        if file.filename == "":

            warning = "⚠ Please choose an image."

            return render_template(
                "index.html",
                warning=warning,
                prediction=None,
                image_path=""
            )

        # Wrong extension
        if not allowed_file(file.filename):

            warning = "⚠ Only JPG, JPEG and PNG images are allowed."

            return render_template(
                "index.html",
                warning=warning,
                prediction=None,
                image_path=""
            )

        filename = secure_filename(file.filename)

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        file.save(filepath)

        global latest_prediction, latest_image

        prediction = predict_image(filepath)

        latest_prediction = prediction
        latest_image = filename

        save_history(filename, prediction)

        image_filename = filename
        

    return render_template(
    "index.html",
    prediction=prediction,
    warning=warning,
    image_filename=image_filename,
    history=load_history()
)

@app.route("/download-report")
def download_report():

    global latest_prediction, latest_image

    if latest_prediction is None:

        return "No prediction available."

    pdf_path = os.path.join(
        REPORT_FOLDER,
        "Prediction_Report.pdf"
    )

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "<b><font size=18>Image Recognition Report</font></b>",
            styles["Title"]
        )
    )

    elements.append(
        Paragraph("<br/>", styles["Normal"])
    )

    elements.append(
        Paragraph(
            f"<b>Image:</b> {latest_image}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>Category:</b> {latest_prediction['category']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>Detail:</b> {latest_prediction['detail']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>Confidence:</b> {latest_prediction['confidence']}%",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>Generated:</b> {datetime.now()}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph("<br/><b>Top 5 Predictions</b>",
                  styles["Heading2"])
    )

    for item in latest_prediction["top5"]:

        elements.append(

            Paragraph(

                f"{item['label']} - {item['confidence']}%",

                styles["Normal"]

            )

        )

    doc.build(elements)

    return send_file(
        pdf_path,
        as_attachment=True
    )


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )

# ==========================
# Delete One History Record
# ==========================

@app.route("/delete_history/<int:index>")
def delete_history(index):

    rows = []

    with open(HISTORY_FILE, "r", newline="", encoding="utf-8") as file:

        reader = csv.reader(file)

        rows = list(reader)

    if len(rows) > 1:

        header = rows[0]

        data = rows[1:]

        if 0 <= index < len(data):

            del data[index]

        with open(HISTORY_FILE, "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow(header)

            writer.writerows(data)

    return redirect("/")


# ==========================
# Clear Entire History
# ==========================

@app.route("/clear_history")
def clear_history():

    with open(HISTORY_FILE, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Image",
            "Category",
            "Detail",
            "Confidence",
            "Time"
        ])

        return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)