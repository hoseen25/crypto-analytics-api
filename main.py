from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal, CryptoPrice
import pydantic

app = FastAPI(title="Crypto Analytics API")

# פונקציית עזר (Dependency) לפתיחה וסגירה אוטומטית של חיבור ל-DB בכל בקשה
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# הגדרת מבנה הנתונים שיחזור למשתמש (Pydantic Model)
class PriceResponse(pydantic.BaseModel):
    coin_name: str
    price_usd: float
    volume_24h: float
    timestamp: str

    class Config:
        from_attributes = True

@app.get("/")
def home():
    return {"status": "healthy", "message": "Welcome to the Crypto Analytics API"}

@app.get("/analytics/{coin_name}")
def get_coin_analytics(coin_name: str, db: Session = Depends(get_db)):
    # שליפת כל הרשומות של המטבע המבוקש מה-DB, מסודר מהחדש ביותר לישן
    records = db.query(CryptoPrice).filter(CryptoPrice.coin_name == coin_name.lower()).order_by(CryptoPrice.timestamp.desc()).all()
    
    if not records:
        raise HTTPException(status_code=404, detail=f"No data found for coin: {coin_name}")
        
    # המרת הנתונים למבנה נקי
    return [
        {
            "coin_name": r.coin_name,
            "price_usd": r.price_usd,
            "volume_24h": r.volume_24h,
            "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        } for r in records
    ]