import os
import PyPDF2
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io


def merge_pdfs_in_folder(folder_path, output_path):
    pdf_writer = PyPDF2.PdfWriter()

    # Check if the folder path exists
    if not os.path.exists(folder_path):
        print(f"Error: The specified path does not exist: {folder_path}")
        return

    # List all PDF files in the given folder
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    pdf_files.sort()  # Sort files for consistent order

    if not pdf_files:
        print("No PDF files found in the specified directory.")
        return

    # Add the pages of each PDF file to the writer object
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_path)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                pdf_writer.add_page(page)
            print(f"Added {pdf_file} to the merger.")
        except Exception as e:
            print(f"Error reading {pdf_file}: {e}")

    # Write the merged PDF to the output path
    try:
        with open(output_path, 'wb') as out_pdf:
            pdf_writer.write(out_pdf)
        print(f"Merged PDF saved as: {output_path}")
    except Exception as e:
        print(f"Error writing output file: {e}")


    # Path where the merged PDF will be saved
    output_pdf = os.path.join(folder_path, 'merged_output.pdf')

    # Merge all PDFs in the specified folder
    merge_pdfs_in_folder(folder_path, output_pdf)



# Path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\wangk.MSI\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def ocr_and_process_pdf(input_pdf_path, output_pdf_path):
    # Open the source PDF
    document = fitz.open(input_pdf_path)
    # Create a new PDF
    new_pdf = fitz.open()

    for page_number in range(len(document)):
        page = document.load_page(page_number)
        text = page.get_text()

        if text.strip():
            # If text is found, add the page directly
            new_pdf.insert_pdf(document, from_page=page_number, to_page=page_number)
            print(f"Page {page_number + 1}: Text found, copying page to new PDF.")
        else:
            print(f"Page {page_number + 1}: No text found, performing OCR.")
            # Render page to an image
            pix = page.get_pixmap()
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            # Perform OCR
            ocr_text = pytesseract.image_to_string(img)

            # Create a new page with OCR text
            new_page = new_pdf.new_page(width=page.rect.width, height=page.rect.height)
            text_insert_position = fitz.Point(50, 50)
            new_page.insert_text(text_insert_position, ocr_text)
            print(f"Page {page_number + 1}: OCR page added to new PDF.")

    # Save the new PDF file
    new_pdf.save(output_pdf_path)
    print(f"OCR processed PDF saved as: {output_pdf_path}")

    
    ocr_and_process_pdf(input_pdf_path, output_pdf_path)
   
if __name__ == "__main__":
    input_pdf_path = r'C:\Users\wangk.MSI\Desktop\pdf_merger\merged_output.pdf'
    output_pdf_path = r'C:\Users\wangk.MSI\Desktop\pdf_merger\ocr_processed_output.pdf'
    ocr_and_process_pdf(input_pdf_path, output_pdf_path)
