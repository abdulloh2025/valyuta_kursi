import mysql.connector

print("MySQL test boshlandi")

conn = mysql.connector.connect(
    host="128.199.149.22",
    port=3306,
    user="remote_user",
    password="StPass#232026!",
    database="hipo",
    connection_timeout=5
)

print("MySQL ulanish OK")
conn.close()
