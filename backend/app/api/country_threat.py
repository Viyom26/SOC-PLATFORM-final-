@router.get("/") # type: ignore
def country_cluster(db: Session = Depends(get_db)): # type: ignore
    results = db.execute("""
        SELECT country, COUNT(*) as count
        FROM alerts
        GROUP BY country
    """).fetchall()

    return [{"country": r[0], "count": r[1]} for r in results]
