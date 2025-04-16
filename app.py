
from flask import Flask, request, jsonify, Response, send_file
from flask_cors import CORS
import csv
from datetime import datetime
import os
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
CORS(app)

EMAILS_FILE = "emails.csv"
PASSWORD_PROTECTION_KEY = "acceso123"  # Cambia esta clave por una segura
EMAIL_FROM = "unmagma@gmail.com"       # <--- Cambia por tu correo real
EMAIL_PASSWORD = "recoño75"   # <--- Usa una contraseña de aplicación (NO tu clave real)
EMAIL_SUBJECT = "Confirmación ElottoIA"
EMAIL_BODY = "Gracias por tu compra. Activaremos tu cuenta en breve. Si tienes dudas, responde a este mensaje."

def enviar_confirmacion(correo):
    try:
        msg = EmailMessage()
        msg.set_content(EMAIL_BODY)
        msg["Subject"] = EMAIL_SUBJECT
        msg["From"] = EMAIL_FROM
        msg["To"] = correo

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_FROM, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print("Error enviando email:", e)
        return False

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

    enviar_confirmacion(email)
    return jsonify({"success": True}), 200

@app.route("/ver-correos", methods=["GET"])
def ver_correos():
    clave = request.args.get("clave")
    if clave != PASSWORD_PROTECTION_KEY:
        return "<h3>⛔ Acceso denegado. Clave incorrecta.</h3>", 403

    if not os.path.exists(EMAILS_FILE):
        return "<h2>No hay correos guardados aún.</h2>"

    html = "<h2>📧 Correos recibidos:</h2><ul>"
    with open(EMAILS_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            html += f"<li>{row[0]} — {row[1]}</li>"
    html += "</ul>"
    return Response(html, mimetype="text/html")

@app.route("/descargar-correos", methods=["GET"])
def descargar_correos():
    clave = request.args.get("clave")
    if clave != PASSWORD_PROTECTION_KEY:
        return "Acceso denegado", 403

    if os.path.exists(EMAILS_FILE):
        return send_file(EMAILS_FILE, as_attachment=True)
    return "No hay archivo para descargar", 404

if __name__ == "__main__":
    app.run(debug=True)
