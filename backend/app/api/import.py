from fastapi import APIRouter, UploadFile, BackgroundTasks
from app.services.excel_processor import process_file

router = APIRouter(prefix="/api/import", tags=["Import"])

@router.post("/")
def import_logs(file: UploadFile, background_tasks: BackgroundTasks):

    background_tasks.add_task(process_file, file)

    return {"status": "Import started in background"}