from io import BytesIO
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import qrcode
from PIL import Image

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/api/qr")
def generate_qr():
    text = request.args.get("text", "")
    if not text:
        return jsonify({"error": "Missing 'text' query parameter"}), 400

    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
    )
    qr.add_data(text)
    qr.make(fit=True)

    # Generate image
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Return QR code image
    return send_file(buffer, mimetype="image/png")

@app.route("/")
def home():
    return jsonify({
        "message": "QR Code API is running ✅",
        "usage": "/api/qr?text=YourTextHere"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
