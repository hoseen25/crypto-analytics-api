import requests
import logging
from database import init_db, SessionLocal, CryptoPrice

# הגדרת לוגים
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_vol=true"

def fetch_and_save_prices():
    try:
        logging.info("מציג בקשה ל-CoinGecko...")
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        logging.info("הנתונים נמשכו בהצלחה. מתחיל לשמור בבסיס הנתונים...")

        # פתיחת סשן (חיבור) ל-DB
        db = SessionLocal()
        
        # מעבר על המטבעות שקיבלנו מה-API ושמירה של כל אחד מהם
        for coin_id, values in data.items():
            price_record = CryptoPrice(
                coin_name=coin_id,
                price_usd=values['usd'],
                volume_24h=values['usd_24h_vol']
            )
            db.add(price_record) # מוסיף לתור
        
        db.commit() # שומר פיזית בבסיס הנתונים
        db.close()  # סוגר את החיבור
        
        logging.info("כל הנתונים נשמרו בבסיס הנתונים בהצלחה!")

    except requests.exceptions.RequestException as err:
        logging.error(f"שגיאה במשיכת הנתונים: {err}")
    except Exception as e:
        logging.error(f"שגיאה בשמירה ל-DB: {e}")

if __name__ == "__main__":
    # 1. ניצור את הטבלאות במידה והן לא קיימות עדיין
    init_db()
    
    # 2. נריץ את המשיכה והשמירה
    fetch_and_save_prices()