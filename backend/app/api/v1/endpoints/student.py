from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class StudentDetailsRequest(BaseModel):
    name: str
    matricule: str
    department: str = None
    level: str = None

@router.post("/details")
async def receive_student_details(details: StudentDetailsRequest):
    """
    Receive and store student details.
    """
    try:
        # In a real app, save to database
        # For now, just echo back
        return {
            "success": True,
            "message": "Student details received successfully",
            "data": {
                "name": details.name,
                "matricule": details.matricule,
                "department": details.department,
                "level": details.level
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
