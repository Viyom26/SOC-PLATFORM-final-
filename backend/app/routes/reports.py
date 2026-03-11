@router.post("/send-report") # pyright: ignore[reportUndefinedVariable]
def send_report(
    db: Session = Depends(get_db), # type: ignore
    user=Depends(require_role("ADMIN")), # pyright: ignore[reportUndefinedVariable]
):
    # generate PDF / Excel from DB
    # send via SMTP
    return {"status": "Report emailed"}
