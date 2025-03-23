from flask import Flask, render_template, request, jsonify
import os
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

app = Flask(__name__)

# Load the processor and model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    question = request.form.get('question', '')

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        image_path = os.path.join('static', 'uploads', file.filename)
        file.save(image_path)

        # Process the image and question
        image = Image.open(image_path).convert("RGB")

        # Preprocess the image and question exactly as in Code 2
        inputs = processor(image, question, return_tensors="pt")

        # Generate the answer with the same parameters as Code 2
        out = model.generate(
            **inputs,
            max_length=50,  # Adjust max_length if needed
            num_beams=5,    # Adjust num_beams if needed
            early_stopping=True  # Enable early stopping
        )

        answer = processor.decode(out[0], skip_special_tokens=True)
        return jsonify({"answer": answer})

if __name__ == '__main__':
    os.makedirs(os.path.join('static', 'uploads'), exist_ok=True)
    app.run(debug=True)