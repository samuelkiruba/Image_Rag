from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

# Load the processor and model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

def ask_question_about_image(image_path, question):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(image, question, return_tensors="pt")
    out = model.generate(**inputs, max_length=50, num_beams=5, early_stopping=True)
    answer = processor.decode(out[0], skip_special_tokens=True)
    return answer

# Test with a sample image and question
image_path = "your_image.jpg"
question = "What is the breed of puppy?"
answer = ask_question_about_image(image_path, question)
print("Answer:", answer)