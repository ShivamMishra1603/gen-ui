from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import PIL.Image
import io
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

UI_GENERATION_PROMPT = os.getenv('UI_GENERATION_PROMPT')
if not UI_GENERATION_PROMPT:
    raise ValueError("UI_GENERATION_PROMPT not found in environment variables")

@app.route('/')
def home():
    return jsonify({"message": "GenUI Backend is running!"})

@app.route('/generate-ui', methods=['POST'])
def generate_ui():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
        file_extension = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        if file_extension not in allowed_extensions:
            return jsonify({"error": "Invalid file type. Please upload an image file."}), 400
        
        image_bytes = file.read()
        img = PIL.Image.open(io.BytesIO(image_bytes))
        
        print("🚀 Generating UI code with Gemini...")
        response = model.generate_content([UI_GENERATION_PROMPT, img])
        
        generated_code = response.text
        
        if "```html" in generated_code:
            generated_code = generated_code.split("```html")[1].split("```")[0].strip()
        elif "```" in generated_code:
            generated_code = generated_code.split("```")[1].split("```")[0].strip()
        
        return jsonify({
            "success": True,
            "html_code": generated_code,
            "message": "UI code generated successfully!"
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
