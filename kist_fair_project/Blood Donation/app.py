from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import openai
import PyPDF2
from PIL import Image
import pytesseract

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

# Configure OpenAI API Key
openai.api_key = "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"  # Replace with your actual key

# Check if the file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for rendering the homepage
@app.route("/")
def home():
    return render_template("index.html")

# Route for uploading and analyzing the blood test report
@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Extract text from file
        if filename.endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        else:
            text = extract_text_from_image(file_path)

        # AI analysis on the extracted text
        analysis = analyze_blood_report(text)
        return jsonify(analysis)

    return jsonify({"error": "Invalid file type"}), 400

# Extract text from PDF
def extract_text_from_pdf(file_path):
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

# Extract text from Image
def extract_text_from_image(file_path):
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    return text

# Analyze blood report using OpenAI
def analyze_blood_report(text):
    prompt = f"Analyze the following blood test report and provide the following details:\n1. Summary of the blood test.\n2. Potential health problems.\n3. Recommendations for diet and lifestyle.\n4. Interesting facts about blood.\n\n{text}\n"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return {"analysis": response["choices"][0]["message"]["content"]}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
