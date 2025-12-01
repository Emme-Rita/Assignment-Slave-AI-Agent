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

file_service = FileService()
