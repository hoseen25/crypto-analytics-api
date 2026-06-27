import requests
import time
import logging

# הגדרת לוגים כדי לראות מה קורה בזמן אמת (דרישה חשובה של אנפורנה!)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_vol=true"

def fetch_crypto_prices():
    try:
        logging.info("מנסה למשוך נתונים מ-CoinGecko...")
        # הגדרת Timeout של 10 שניות כדי למנוע מהתוכנה להיתקע אם הרשת איטית
        response = requests.get(URL, timeout=10)
        
        # אם ה-API החזיר שגיאה (כמו 429 או 500), זה יקפיץ שגיאה ישירות ל-except
        response.raise_for_status()
        
        data = response.json()
        logging.info("הנתונים נמשכו בהצלחה!")
        return data

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"שגיאת HTTP (ייתכן שהגענו למגבלת הראט-לימיט): {http_err}")
    except requests.exceptions.Timeout:
        logging.error("שגיאה: הבקשה ל-API לקחה יותר מדי זמן (Timeout)")
    except requests.exceptions.RequestException as err:
        logging.error(f"שגיאה כללית בתקשורת: {err}")
    
    return None

if __name__ == "__main__":
    # נריץ בדיקה ראשונית
    data = fetch_crypto_prices()
    if data:
        print("\n--- הנתונים שהתקבלו ---")
        print(data)