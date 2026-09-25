import PyPDF2
import sys
import io

try:
    # Set UTF-8 encoding for stdout
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')

    pdf_file = open('update price list.pdf', 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Extract text from all pages
    for page_num, page in enumerate(pdf_reader.pages):
        text = page.extract_text()
        print(f"--- Page {page_num + 1} ---")
        print(text)
        print()

    pdf_file.close()

except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
