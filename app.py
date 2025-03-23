from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from PIL import Image
from transformers import BlipProcessor, BlipForQuestionAnswering
import torch

# Initialize Flask app
app = Flask(__name__)

# Load the BLIP processor and model for VQA
processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")

# Ensure the uploads directory exists
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    """
    Renders the home page with the image question-answering form.
    """
    return render_template('index.html')

@app.route('/feedback')
def feedback():
    """
    Renders the feedback page where users can submit feedback.
    """
    return render_template('feedback.html')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    """
    Handles feedback form submission.
    """
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # Here you can save the feedback to a database or send it via email
    print(f"Feedback received from {name} ({email}): {message}")

    # Redirect to a thank-you page or back to the home page
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload_image():
    """
    Handles image upload and question-answering.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    question = request.form.get('question', '')

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        try:
            # Save the uploaded image
            image_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(image_path)

            # Load and preprocess the image
            image = Image.open(image_path).convert("RGB")

            # Debugging: Print image details
            print(f"Image loaded: {image.size} (width x height)")

            # Preprocess the image and question
            inputs = processor(image, question, return_tensors="pt")

            # Debugging: Print processed inputs
            print(f"Processed inputs: {inputs}")

            # Generate the answer
            out = model.generate(
                **inputs,
                max_length=50,  # Adjust based on expected answer length
                num_beams=5,    # Increase for better quality (slower)
                early_stopping=True,  # Stop generation if the model is confident
            )

            # Decode the generated answer
            answer = processor.decode(out[0], skip_special_tokens=True)

            # Debugging: Print the generated answer
            print(f"Generated answer: {answer}")

            return jsonify({"answer": answer})

        except Exception as e:
            # Debugging: Print the error
            print(f"Error: {str(e)}")
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)