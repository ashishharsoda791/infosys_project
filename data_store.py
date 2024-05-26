import cv2
import pytesseract
import csv
import xlsxwriter
import os

# Setting Tesseract path (adjust as necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresholded_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return thresholded_image

def extract_text_from_image(image_path):
    # Check if the file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"The file {image_path} does not exist.")
    
    image = cv2.imread(image_path)
    
    # Check if the image was loaded correctly
    if image is None:
        raise ValueError(f"Failed to load image from path: {image_path}")
    
    processed_image = preprocess_image(image)
    extracted_text = pytesseract.image_to_string(processed_image)
    return extracted_text

def parse_extracted_text(extracted_text):
    amount = ""
    date = ""
    payee_name = ""

    for line in extracted_text.strip().split('\n'):
        line = line.lower()
        if "rupees" in line:
            amount = line.split("rupees")[1].strip()
        elif "pay" in line:
            payee_name = line.split("pay")[1].strip()
        elif "date" in line:
            date = line.replace("date", "").strip()
        elif "payee" in line:
            payee_name = line.split("payee")[1].strip()

    return {
        "Amount": amount,
        "Date": date,
        "Payee Name": payee_name
    }

def write_to_csv(data, csv_file):
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data.keys())
        writer.writerow(data.values())
    print("Successfully written to CSV")

def csv_to_excel(csv_file, excel_file):
    workbook = xlsxwriter.Workbook(excel_file)
    worksheet = workbook.add_worksheet()

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row_idx, row in enumerate(reader):
            for col_idx, cell in enumerate(row):
                worksheet.write(row_idx, col_idx, cell)

    workbook.close()
    print("Successfully converted CSV to Excel")

def export_data(data, format):
    if format == "CSV":
        csv_file = "extracted_data.csv"
        write_to_csv(data, csv_file)
    elif format == "Excel":
        csv_file = "extracted_data.csv"
        excel_file = "extracted_data.xlsx"
        write_to_csv(data, csv_file)
        csv_to_excel(csv_file, excel_file)
    else:
        print("Invalid format specified")

# Main function to extract data from an image and export it
def main(image_path, export_format):
    try:
        extracted_text = extract_text_from_image(image_path)
        parsed_data = parse_extracted_text(extracted_text)
        export_data(parsed_data, export_format)
    except Exception as e:
        print(f"Error: {e}")

# Example usage
image_path = "image_1.jpg"
export_format = "Excel" 
main(image_path, export_format)
