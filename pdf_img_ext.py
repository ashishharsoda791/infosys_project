import fitz  # PyMuPDF

def pdf_to_images(pdf_path, output_folder):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Iterate through each page in the PDF
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()  # Render the page to an image

        # Define the output image file path
        output_image_path = f"{output_folder}/image_{page_num + 1}.jpg"

        # Save the image
        pix.save(output_image_path)
        print(f"Saved {output_image_path}")

# Example usage
pdf_path = "E:/Bank_cheque_ext/Sample.pdf"
output_folder = "E:\Bank_cheque_ext"
pdf_to_images(pdf_path, output_folder)
