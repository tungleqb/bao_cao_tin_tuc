from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import report_type as schema
from ..crud import report_type as crud
from ..dependencies.auth import get_current_admin
from ..database import get_db

router = APIRouter(prefix="/admin/loaibaocao", tags=["Admin-LoaiBaoCao"])

@router.post("/", response_model=schema.ReportTypeOut)
async def create(report_type_in: schema.ReportTypeCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_admin)):
    try:
        return await crud.create_report_type(db, report_type_in)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating report type: {str(e)}")

@router.get("/", response_model=list[schema.ReportTypeOut])
async def read_all(db: AsyncSession = Depends(get_db), user=Depends(get_current_admin)):
    try:
        return await crud.get_report_types(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching report types: {str(e)}")   

@router.put("/{id}", response_model=schema.ReportTypeOut)
async def update(id: str, report_type_in: schema.ReportTypeUpdate, db: AsyncSession = Depends(get_db), user=Depends(get_current_admin)):
    try:
        old = await crud.get_report_type(db, id)
        if not old:
            raise HTTPException(status_code=404, detail="ReportType not found")
        await crud.update_report_type(db, id, report_type_in)
        updated = await crud.get_report_type(db, id)
        return updated
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating report type: {str(e)}")

@router.delete("/{id}")
async def delete(id: str, db: AsyncSession = Depends(get_db), user=Depends(get_current_admin)):
    try:
        old = await crud.get_report_type(db, id)
        if not old:
            raise HTTPException(status_code=404, detail="ReportType not found")
        await crud.delete_report_type(db, id)
        return {"msg": "Deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting report type: {str(e)}")
