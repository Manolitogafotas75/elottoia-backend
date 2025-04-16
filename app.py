
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import csv
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

EMAILS_FILE = "emails.csv"

@app.route("/email", methods=["POST"])
def save_email():
    data = request.get_json()
    email = data.get("email", "").strip()
    if not email:
        return jsonify({"error": "Email vacío"}), 400

    timestamp = datetime.now().isoformat()
    with open(EMAILS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, email])

    return jsonify({"success": True}), 200

@app.route("/ver-correos", methods=["GET"])
def ver_correos():
    if not os.path.exists(EMAILS_FILE):
        return "<h2>No hay correos guardados aún.</h2>"

    html = "<h2>📧 Correos recibidos:</h2><ul>"
    with open(EMAILS_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            html += f"<li>{row[0]} — {row[1]}</li>"
    html += "</ul>"
    return Response(html, mimetype="text/html")

if __name__ == "__main__":
    app.run(debug=True)
