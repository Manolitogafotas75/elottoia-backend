from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/submit-email', methods=['POST'])
def submit_email():
    data = request.get_json()
    email = data.get('email')
    if email:
        with open('emails.txt', 'a') as f:
            f.write(f"{datetime.now().isoformat()} - {email}\n")
        return jsonify({"success": True, "message": "Email guardado correctamente."})
    return jsonify({"success": False, "message": "Email no válido."}), 400

if __name__ == '__main__':
    app.run(debug=True)
