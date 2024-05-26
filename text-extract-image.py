import pytesseract
from PIL import Image, ImageEnhance, ImageFilter


def preprocess_image(image_path):
    img = Image.open(image_path)
    
    # Convert image to grayscale
    img = img.convert('L')
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)
    
    # Apply a slight blur to reduce noise
    img = img.filter(ImageFilter.MedianFilter())
    
    return img

def image_to_text(image_path):
    # Preprocess the image
    img = preprocess_image(image_path)
    
    # Perform OCR using PyTesseract
    text = pytesseract.image_to_string(img)
    
    return text

image_path = 'image_1.jpg'  
extracted_text = image_to_text(image_path)
print(extracted_text)