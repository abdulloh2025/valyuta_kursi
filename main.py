# import os
# from dotenv import load_dotenv
# import mysql.connector
# import requests
# from datetime import datetime
#
# load_dotenv()
#
# # MySQL конфигурация
# config = {
#     "host": os.getenv("DB_HOST"),
#     "port": int(os.getenv("DB_PORT")),
#     "user": os.getenv("DB_USER"),
#     "password": os.getenv("DB_PASSWORD"),
#     "database": os.getenv("DB_NAME"),
#     "auth_plugin": "mysql_native_password"
# }
#
# # CBU валюта курси API (масалан, XML ёки JSON)
# CBU_URL = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
#
# def get_currency_rates():
#     response = requests.get(CBU_URL)
#     response.raise_for_status()
#     return response.json()  # JSON рўйхатини олади
#
# def save_rates_to_db(rates):
#     conn = mysql.connector.connect(**config)
#     cursor = conn.cursor()
#     for item in rates:
#         currency = item['Ccy']
#         rate = float(item['Rate'])
#         # Тўғри форматлаш
#         date = datetime.strptime(item['Date'], "%d.%m.%Y").date()
#         cursor.execute("""
#             INSERT INTO valyuta_kursi (currency_code, rate, date)
#             VALUES (%s, %s, %s)
#         """, (currency, rate, date))
#
#     conn.commit()
#     cursor.close()
#     conn.close()
#
# if __name__ == "__main__":
#     rates = get_currency_rates()
#     save_rates_to_db(rates)
#     print("CBU курслари базага ёзилди.")
