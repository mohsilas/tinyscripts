import pytesseract
from pdf2image import convert_from_path
import os
from PIL import Image
import argparse
import sys
from shutil import which
import threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def check_dependencies():
    """
    Check if required external dependencies are installed.
    """
    # Check for poppler
    if sys.platform.startswith('win'):
        # On Windows, check if poppler is in PATH
        if not any(os.path.exists(os.path.join(path, 'pdftoppm.exe'))
                  for path in os.environ["PATH"].split(os.pathsep)):
            print("Error: poppler-utils is not installed or not in PATH.")
            print("Please download poppler for Windows from:")
            print("https://github.com/oschwartz10612/poppler-windows/releases/")
            print("Extract it and add the 'bin' directory to your PATH.")
            return False
    else:
        # On Unix-like systems, check for pdftoppm
        if which('pdftoppm') is None:
            print("Error: poppler-utils is not installed.")
            print("For Ubuntu/Debian: sudo apt-get install poppler-utils")
            print("For macOS: brew install poppler")
            return False

    # Check for Tesseract
    try:
        pytesseract.get_tesseract_version()
    except pytesseract.TesseractNotFoundError:
        print("Error: Tesseract is not installed or not in PATH.")
        print("For Windows: Download and install from GitHub releases")
        print("For Ubuntu/Debian: sudo apt-get install tesseract-ocr")
        print("For macOS: brew install tesseract")
        return False

    return True

class PageProcessor:
    def __init__(self, temp_dir):
        self.temp_dir = temp_dir
        self.results = {}
        self.lock = threading.Lock()

    def process_page(self, args):
        """
        Process a single page with OCR.
        """
        page_num, image = args
        try:
            # Save the image temporarily with a thread-safe filename
            thread_id = threading.get_ident()
            image_path = os.path.join(self.temp_dir, f"page_{page_num}_thread_{thread_id}.png")

            image.save(image_path, 'PNG')

            # Perform OCR on the image
            page_text = pytesseract.image_to_string(Image.open(image_path))

            # Clean up temporary image
            os.remove(image_path)

            # Store the result in a thread-safe manner
            with self.lock:
                self.results[page_num] = page_text
                print(f"Completed page {page_num}")

            return page_num, page_text

        except Exception as e:
            print(f"Error processing page {page_num}: {str(e)}")
            return page_num, ""

def extract_text_from_pdf(pdf_path, output_file=None, max_threads=None):
    """
    Extract text from a PDF file using OCR with multi-threading.

    Args:
        pdf_path (str): Path to the PDF file
        output_file (str): Optional path to save the extracted text
        max_threads (int): Maximum number of threads to use (default: CPU count)

    Returns:
        str: Extracted text from the PDF
    """
    try:
        # Check dependencies first
        if not check_dependencies():
            return None

        # Check if PDF file exists
        if not os.path.exists(pdf_path):
            print(f"Error: PDF file not found: {pdf_path}")
            return None

        start_time = time.time()

        # Convert PDF to images
        print(f"Converting PDF to images: {pdf_path}")
        images = convert_from_path(pdf_path)
        print(f"Found {len(images)} pages")

        # Create a temporary directory for images if it doesn't exist
        temp_dir = 'temp_ocr_images'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # Initialize the page processor
        processor = PageProcessor(temp_dir)

        # Determine the number of threads to use
        if max_threads is None:
            import multiprocessing
            max_threads = multiprocessing.cpu_count()

        print(f"Processing with {max_threads} threads")

        # Process pages in parallel using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            # Submit all pages for processing
            future_to_page = {
                executor.submit(processor.process_page, (i + 1, image)): i + 1
                for i, image in enumerate(images)
            }

            # Wait for all tasks to complete
            for future in as_completed(future_to_page):
                page_num = future_to_page[future]
                try:
                    future.result()
                except Exception as e:
                    print(f"Error processing page {page_num}: {str(e)}")

        # Combine results in correct order
        extracted_text = ""
        for i in range(1, len(images) + 1):
            if i in processor.results:
                extracted_text += f"\n\n--- Page {i} ---\n\n" + processor.results[i]

        # Clean up temporary directory
        os.rmdir(temp_dir)

        # Calculate processing time
        end_time = time.time()
        processing_time = end_time - start_time
        print(f"\nProcessing completed in {processing_time:.2f} seconds")

        # Save to file if output path is provided
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(extracted_text)
            print(f"Extracted text saved to: {output_file}")

        return extracted_text

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Extract text from PDF using OCR')
    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument('--output', '-o', help='Path to save the extracted text')
    parser.add_argument('--threads', '-t', type=int, help='Number of threads to use')

    args = parser.parse_args()

    # Extract text
    extracted_text = extract_text_from_pdf(args.pdf_path, args.output, args.threads)

    if extracted_text and not args.output:
        print("\nExtracted Text:")
        print(extracted_text)

if __name__ == "__main__":
    main()
