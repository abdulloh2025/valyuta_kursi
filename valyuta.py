import os
import logging
from dotenv import load_dotenv
import pymysql  # <--- O'ZGARD (mysql.connector o'rniga)
import requests
from datetime import datetime

# --- Logging sozlash ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# --- .env yuklash ---
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# --- .env tekshirish ---
if not all([DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME]):
    logging.error(".env ichidagi ma'lumotlar to‘liq emas!")
    exit(1)

# PyMySQL uchun konfiguratsiya
config = {
    "host": DB_HOST,
    "port": int(DB_PORT),
    "user": DB_USER,
    "password": DB_PASSWORD,
    "database": DB_NAME,
    "cursorclass": pymysql.cursors.DictCursor,  # Natijani dict ko'rinishida olish uchun
    "connect_timeout": 10
}

# --- API URL ---
CBU_URL = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"


# --- Valyuta kurslarini olish ---
def get_currency_rates():
    logging.info("API so‘rov yuborilyapti...")
    response = requests.get(CBU_URL, timeout=10)
    response.raise_for_status()
    data = response.json()
    logging.info(f"API dan {len(data)} ta valyuta keldi")
    return data


# --- Bazaga saqlash ---
def save_rates_to_db(rates):
    conn = None
    cursor = None
    try:
        logging.info("MySQL ga ulanilyapti (PyMySQL)...")
        # Ulanishni yaratish
        conn = pymysql.connect(**config)
        cursor = conn.cursor()

        saved_count = 0
        for item in rates:
            currency = item.get('Ccy')
            rate = float(item.get('Rate', 0))
            date_str = item.get('Date')

            # Sana formatini to'g'irlash (API: 27.01.2026 -> MySQL: 2026-01-27)
            date = None
            if date_str:
                date = datetime.strptime(date_str, "%d.%m.%Y").strftime("%Y-%m-%d")

            # SQL so'rov
            sql = """
                INSERT INTO valyuta_kursi (currency_code, rate, date)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE rate=%s
            """
            cursor.execute(sql, (currency, rate, date, rate))
            saved_count += 1

        conn.commit()
        logging.info(f"{saved_count} ta yozuv bazaga saqlandi")

    except pymysql.MySQLError as err:  # PyMySQL xatolarini tutish
        logging.error(f"MySQL xatosi: {err}")

    except Exception as err:
        logging.error(f"Noma’lum xato: {err}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            logging.info("MySQL bilan aloqa uzildi.")


# --- Main blok ---
if __name__ == "__main__":
    logging.info("Programma ishga tushdi")
    try:
        rates = get_currency_rates()
        save_rates_to_db(rates)
        logging.info("Programma muvaffaqiyatli yakunlandi")
    except requests.RequestException as e:
        logging.error(f"API so‘rov xatosi: {e}")
    except Exception as e:
        logging.error(f"Noma’lum xato: {e}")