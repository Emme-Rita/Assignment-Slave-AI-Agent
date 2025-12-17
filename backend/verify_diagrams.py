from app.services.file_service import file_service
import os

markdown_content = """# Process Flow

Here is the flow diagram:

```
Start -> A -> B -> C
              |
              v
              D -> Finish
```

And some normal text.
"""

student_data = {
    "name": "Jane Student",
    "matricule": "FE23A456",
    "school": "University of Buea",
    "level": "Level 400",
    "department": "Computer Science"
}

try:
    print("Generating DOCX with Diagram...")
    filepath = file_service.generate_docx(markdown_content, "diagram_test.docx", student_info=student_data)
    print(f"✅ File created at: {filepath}")
    print("Please open this file and verify:")
    print("1. The diagram is in Courier New (Monospace).")
    print("2. The diagram alignment is preserved.")
except Exception as e:
    print(f"❌ Error: {e}")
