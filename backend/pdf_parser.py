import pdfplumber

def parse_pdf(file_path):
    """
    Parses a pdf file and returns the content as a string
    """
    with pdfplumber.open(file_path) as pdf:
        content = []
        for page in pdf.pages:
            content.append(page.extract_text())
        return "\n".join(content)
