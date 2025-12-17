from app.services.file_service import file_service
import os

markdown_content = """# Assignment Title

## Introduction
This is a **test document** to verify formatting.

### Data Analysis
Here is a table of data:

| Metric | Value | Unit |
|---|---|---|
| Speed | 100 | km/h |
| Weight | 50 | kg |
| Efficiency | 95% | N/A |

### Conclusion
- Point A
- Point B with **bold text**
"""

try:
    print("Generating formatted DOCX...")
    filepath = file_service.generate_docx(markdown_content, "formatting_test.docx")
    print(f"✅ File created at: {filepath}")
    print("Please open this file and verify:")
    print("1. 'Assignment Title' is a Heading 1")
    print("2. 'Introduction' is a Heading 2")
    print("3. There is a real Table (not text with | )")
    print("4. 'test document' is BOLD")
except Exception as e:
    print(f"❌ Error: {e}")
