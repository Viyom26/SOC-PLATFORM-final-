from fastapi import APIRouter
from app.services.gpt_service import analyze_log, summarize_logs
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from sqlalchemy import text
router = APIRouter()


@router.post("/logs/ai-explain")
def ai_explain(log: dict):
    result = analyze_log(log)

    return {
        "result": {
            "type": "Network Attack",
            "risk": "HIGH",
            "explanation": result,
            "action": "Investigate source IP immediately"
        }
    }

@router.get("/logs/summary")
def ai_summary(db: Session = Depends(get_db)):
    logs = db.execute(
        text("SELECT * FROM logs ORDER BY created_at DESC LIMIT 50")
    ).fetchall()

    logs_list = [dict(row._mapping) for row in logs]

    return {"summary": summarize_logs(logs_list)}