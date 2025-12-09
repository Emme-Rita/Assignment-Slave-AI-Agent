from fastapi import APIRouter, HTTPException
from app.services.history_service import history_service

router = APIRouter()

@router.get("/history")
async def get_history(limit: int = 50):
    """
    Get all assignment execution history.
    
    Args:
        limit: Maximum number of records to return
        
    Returns:
        List of history records
    """
    try:
        records = await history_service.get_all_history(limit=limit)
        return {
            "success": True,
            "data": records,
            "count": len(records)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{record_id}")
async def get_history_details(record_id: str):
    """
    Get detailed information about a specific execution.
    
    Args:
        record_id: ID of the execution record
        
    Returns:
        Detailed execution data
    """
    try:
        details = await history_service.get_execution_details(record_id)
        if not details:
            raise HTTPException(status_code=404, detail="Record not found")
        
        return {
            "success": True,
            "data": details
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/history/{record_id}")
async def delete_history_record(record_id: str):
    """
    Delete an execution record from history.
    
    Args:
        record_id: ID of the record to delete
        
    Returns:
        Success status
    """
    try:
        deleted = await history_service.delete_execution(record_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Record not found")
        
        return {
            "success": True,
            "message": "Record deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
