from fastapi import UploadFile, HTTPException
from typing import Optional
import mimetypes

class FileService:
    ALLOWED_EXTENSIONS = {
        'image': ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
        'pdf': ['application/pdf'],
        'word': [
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/msword'
        ]
    }
    
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    @staticmethod
    async def validate_file(file: UploadFile) -> bool:
        """
        Validate uploaded file type and size.
        
        Args:
            file: Uploaded file
        
        Returns:
            True if valid
        
        Raises:
            HTTPException if invalid
        """
        # Check file size
        file_content = await file.read()
        await file.seek(0)  # Reset file pointer
        
        if len(file_content) > FileService.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds maximum allowed size of {FileService.MAX_FILE_SIZE / (1024*1024)}MB"
            )
        
        # Check file type
        content_type = file.content_type
        all_allowed = (
            FileService.ALLOWED_EXTENSIONS['image'] +
            FileService.ALLOWED_EXTENSIONS['pdf'] +
            FileService.ALLOWED_EXTENSIONS['word']
        )
        
        if content_type not in all_allowed:
            raise HTTPException(
                status_code=400,
                detail=f"File type {content_type} not allowed. Allowed types: images, PDF, Word documents"
            )
        
        return True
    
    @staticmethod
    def get_file_category(content_type: str) -> str:
        """Determine file category from content type."""
        if content_type in FileService.ALLOWED_EXTENSIONS['image']:
            return 'image'
        elif content_type in FileService.ALLOWED_EXTENSIONS['pdf']:
            return 'pdf'
        elif content_type in FileService.ALLOWED_EXTENSIONS['word']:
            return 'word'
        return 'unknown'

    @staticmethod
    def generate_pdf(content: str, filename: str) -> str:
        """
        Generate a PDF file from text content.
        
        Args:
            content: The text content to write
            filename: The output filename
            
        Returns:
            Absolute path to the generated file
        """
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            from reportlab.lib.utils import simpleSplit
            import os
            
            # Ensure output directory exists - save to temp dir or specific outputs dir
            output_dir = os.path.join(os.getcwd(), "outputs")
            os.makedirs(output_dir, exist_ok=True)
            
            filepath = os.path.join(output_dir, filename)
            
            c = canvas.Canvas(filepath, pagesize=letter)
            width, height = letter
            
            # Simple text wrapping
            text_object = c.beginText(40, height - 40)
            text_object.setFont("Helvetica", 12)
            
            lines = content.split('\n')
            for line in lines:
                # Wrap long lines
                wrapped_lines = simpleSplit(line, "Helvetica", 12, width - 80)
                for wrapped_line in wrapped_lines:
                    # Check if we need a new page
                    if text_object.getY() < 40:
                        c.drawText(text_object)
                        c.showPage()
                        text_object = c.beginText(40, height - 40)
                        text_object.setFont("Helvetica", 12)
                    text_object.textLine(wrapped_line)
            
            c.drawText(text_object)
            c.save()
            
            return filepath
        except Exception as e:
            raise Exception(f"PDF generation error: {str(e)}")

    @staticmethod
    def generate_docx(content: str, filename: str) -> str:
        """
        Generate a Word document from text content.
        
        Args:
            content: The text content to write
            filename: The output filename
            
        Returns:
            Absolute path to the generated file
        """
        try:
            import docx
            import os
            
            # Ensure output directory exists
            output_dir = os.path.join(os.getcwd(), "outputs")
            os.makedirs(output_dir, exist_ok=True)
            
            filepath = os.path.join(output_dir, filename)
            
            doc = docx.Document()
            
            # Add content preserving paragraphs
            for line in content.split('\n'):
                if line.strip():
                    doc.add_paragraph(line)
            
            doc.save(filepath)
            
            return filepath
        except Exception as e:
            raise Exception(f"DOCX generation error: {str(e)}")

file_service = FileService()
