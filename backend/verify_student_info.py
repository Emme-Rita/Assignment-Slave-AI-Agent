from app.services.file_service import file_service
import os

markdown_content = """# Assignment Title

## Introduction
Content goes here...
"""

student_data = {
    "name": "Jane Student",
    "matricule": "FE23A456",
    "level": "University Year 2",
    "department": "Computer Science"
}

try:
    print("Generating DOCX with Student Info...")
    filepath = file_service.generate_docx(markdown_content, "student_info_test.docx", student_info=student_data)
    print(f"✅ File created at: {filepath}")
    print("Please open this file and verify:")
    print("1. Top of page shows Name, Matricule, etc.")
    print("2. Labels are BOLD.")
except Exception as e:
    print(f"❌ Error: {e}")
