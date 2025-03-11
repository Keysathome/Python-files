import os
import fitz  # PyMuPDF


# Paths (Update these paths as needed)
INPUT_FOLDER = r"C:\Users\aguo1\Documents\coding_projects\pdf_project\test_data"
OUTPUT_FILE = os.path.join(INPUT_FOLDER, "combined.pdf")
TEXT_OUTPUT_FILE = os.path.join(INPUT_FOLDER, "extracted_text.txt")  # Optional text output file


def combine_pdfs(input_folder, output_file):
    """
    Combines all PDF files in the specified folder into a single PDF file.

    Parameters:
        input_folder (str): The path to the folder containing PDF files.
        output_file (str): The path for the combined PDF output.
    """
    output_pdf = fitz.open()

    try:
        pdf_files = sorted(f for f in os.listdir(input_folder) if f.lower().endswith('.pdf'))

        if not pdf_files:
            print("No PDF files found in the specified folder.")
            return

        print(f"Found {len(pdf_files)} PDF files. Combining...")

        for pdf in pdf_files:
            file_path = os.path.join(input_folder, pdf)
            print(f"Adding: {file_path}")

            try:
                input_pdf = fitz.open(file_path)
            except Exception as e:
                print(f"Error opening {file_path}: {e}. Skipping...")
                continue

            output_pdf.insert_pdf(input_pdf)
            input_pdf.close()

        output_pdf.save(output_file)
        print(f"Combined PDF saved as: {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        output_pdf.close()


def extract_text_from_pdf(pdf_file, output_text_file=None):
    """
    Extracts text from a PDF file and optionally saves it to a text file.

    Parameters:
        pdf_file (str): The path to the PDF file to extract text from.
        output_text_file (str): The path for the text file output (optional).
    
    Returns:
        str: The extracted text.
    """
    try:
        doc = fitz.open(pdf_file)
        extracted_text = ""

        print(f"Extracting text from: {pdf_file}")

        for page_number in range(len(doc)):
            page = doc[page_number]
            page_text = page.get_text()
            extracted_text += page_text
            print(f"Extracted text from page {page_number + 1}.")

        doc.close()

        if output_text_file:
            with open(output_text_file, "w", encoding="utf-8") as text_file:
                text_file.write(extracted_text)
            print(f"Extracted text saved to: {output_text_file}")

        return extracted_text

    except Exception as e:
        print(f"An error occurred while extracting text: {e}")
        return ""


if __name__ == "__main__":
    # Combine PDFs
    combine_pdfs(INPUT_FOLDER, OUTPUT_FILE)

    # Extract text from the combined PDF
    extract_text_from_pdf(OUTPUT_FILE, TEXT_OUTPUT_FILE)
