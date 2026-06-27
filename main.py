from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func  # ייבוא פונקציות ה-SQL (כמו AVG, MIN, MAX)
from database import SessionLocal, CryptoPrice, init_db
from fetcher import fetch_and_save_prices
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
import logging

# הגדרת לוגים כדי לראות את האוטומציה עובדת
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 1. הגדרת ה-Lifespan: מה קורה כשהשרת נדלק וכשהוא נכבה
@asynccontextmanager
async def lifespan(app: FastAPI):
    # קוד שרץ כשהשרת *מתחיל*
    init_db() # ודואג שבסיס הנתונים מוכן
    
    # הגדרת המערכת האוטומטית (Scheduler)
    scheduler = BackgroundScheduler()
    # נגדיר שהיא תריץ את פונקציית המשיכה והשמירה בכל 1 דקה (בשביל הבדיקה, אחרי זה נשנה ל-5 או 10 דקות)
    scheduler.add_job(fetch_and_save_prices, 'interval', minutes=1)
    scheduler.start()
    logging.info("⏱️ ה-Worker האוטומטי הופעל בהצלחה! משיכת נתונים תתבצע כל דקה.")
    
    yield # כאן השרת ממשיך לעבוד כרגיל ולקבל בקשות
    
    # קוד שרץ כשהשרת *נסגר*
    scheduler.shutdown()
    logging.info("🛑 ה-Worker האוטומטי נעצר.")

# נחבר את ה-lifespan לאפליקציה
app = FastAPI(title="Crypto Analytics API", lifespan=lifespan)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"status": "healthy", "message": "Welcome to the Automated Crypto Analytics API"}

@app.get("/analytics/{coin_name}")
def get_coin_analytics(coin_name: str, db: Session = Depends(get_db)):
    records = db.query(CryptoPrice).filter(CryptoPrice.coin_name == coin_name.lower()).order_by(CryptoPrice.timestamp.desc()).all()
    if not records:
        raise HTTPException(status_code=404, detail=f"No data found for coin: {coin_name}")
    
    return [
        {
            "coin_name": r.coin_name,
            "price_usd": r.price_usd,
            "volume_24h": r.volume_24h,
            "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        } for r in records
    ]

# 🔥 נקודת הקצה החדשה לאנליטיקה וסטטיסטיקות
@app.get("/analytics/{coin_name}/stats")
def get_coin_stats(coin_name: str, db: Session = Depends(get_db)):
    # הרצת שאילתת אגרגציה (Aggregation) ישירות בתוך בסיס הנתונים
    stats = db.query(
        func.avg(CryptoPrice.price_usd).label("average_price"),
        func.min(CryptoPrice.price_usd).label("min_price"),
        func.max(CryptoPrice.price_usd).label("max_price"),
        func.count(CryptoPrice.id).label("total_samples")
    ).filter(CryptoPrice.coin_name == coin_name.lower()).first()

    # אם בסיס הנתונים לא מצא אף רשומה למטבע הזה
    if not stats or stats.total_samples == 0:
        raise HTTPException(status_code=404, detail=f"No stats available for coin: {coin_name}")

    return {
        "coin_name": coin_name.lower(),
        "total_samples_analyzed": stats.total_samples,
        "metrics": {
            "average_price_usd": round(stats.average_price, 2) if stats.average_price else 0,
            "min_price_usd": round(stats.min_price, 2) if stats.min_price else 0,
            "max_price_usd": round(stats.max_price, 2) if stats.max_price else 0,
            "volatility_detected": stats.max_price != stats.min_price
        }
    }