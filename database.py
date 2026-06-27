from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# נתיב לקובץ בסיס הנתונים (ייווצר אוטומטית בתיקייה)
DATABASE_URL = "sqlite:///./crypto.db"

# יצירת המנוע שמדבר עם ה-DB
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# יצירת סשן (Session) שדרכו נבצע פעולות (הכנסה, שליפה)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# הגדרת הטבלה שבה נשמור את מחירי הקריפטו
class CryptoPrice(Base):
    __tablename__ = "crypto_prices"

    id = Column(Integer, primary_key=True, index=True)
    coin_name = Column(String, index=True)         # שם המטבע (bitcoin, solana...)
    price_usd = Column(Float)                      # מחיר בדולר
    volume_24h = Column(Float)                     # נפח מסחר ב-24 שעות האחרונות
    timestamp = Column(DateTime, default=datetime.utcnow) # זמן שמירת הנתון

# פונקציה ליצירת הטבלאות בפועל בתוך הקובץ
def init_db():
    Base.metadata.create_all(bind=engine)