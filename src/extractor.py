import os
import re
from PyPDF2 import PdfReader
from docx import Document

class ResumeExtractor:
    def __init__(self, input_folder):
        self.input_folder = input_folder

    def extract_text(self, file_path):
        if file_path.endswith(".pdf"):
            return self._extract_pdf_text(file_path)
        elif file_path.endswith(".docx"):
            return self._extract_docx_text(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")

    def _extract_pdf_text(self, file_path):
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    def _extract_docx_text(self, file_path):
        doc = Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])

    def clean_text(self, text):
        try:
            # Remove non-printable characters
            text = re.sub(r'[^\x20-\x7E]', '', text)
            
            # Remove extra whitespace, tabs, and newlines
            text = re.sub(r'\s+', ' ', text).strip()

            # Handle unterminated strings or incomplete lines
            text = text.replace('“', '"').replace('”', '"').replace("’", "'")

            # Ensure balanced quotes and brackets (if JSON-like structures exist)
            if text.count('"') % 2 != 0:
                text = text.rsplit('"', 1)[0]  # Remove unbalanced quote

            return text
        except Exception as e:
            print(f"Error cleaning text: {e}")
            return None

    def get_all_files(self):
        return [os.path.join(self.input_folder, f) for f in os.listdir(self.input_folder) if f.endswith(('.pdf', '.docx'))]


class JdExtractor(ResumeExtractor):
    def extract_text(self, file_path):

        print(f"Extracting text from JD file: {file_path}")
        return super().extract_text(file_path)

    def get_all_files(self):
        files = super().get_all_files()
        print(f"Found {len(files)} JD files in the folder.")
        return files
