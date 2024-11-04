from flask import Flask, g
from datetime import datetime
import pyodbc

# تنظیمات اتصال به SQL Server
DATABASE_CONFIG = {
    'server': 'SHAFAFTVEDC-SRV',
    'database': 'sunergy',
    'username': 'sunergy',
    'password': 'Sun@2412%$#'
}

app = Flask(__name__)  # ایجاد نمونه ای از اپلیکیشن Flask

# تابع دسترسی به دیتابیس
def get_db():
    if 'db' not in g:
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={DATABASE_CONFIG['server']};"
            f"DATABASE={DATABASE_CONFIG['database']};"
            f"UID={DATABASE_CONFIG['username']};"
            f"PWD={DATABASE_CONFIG['password']}"
        )
        g.db = pyodbc.connect(connection_string)
    return g.db

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        # ایجاد جدول stats اگر وجود نداشته باشد
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='stats' AND xtype='U')
            BEGIN
                CREATE TABLE stats (
                    id INT PRIMARY KEY IDENTITY(1,1),
                    visits INT DEFAULT 0,
                    last_update NVARCHAR(50)
                )
                -- افزودن یک رکورد اولیه با تعداد بازدید صفر و تاریخ فعلی
                INSERT INTO stats (visits, last_update) VALUES (0, ?)
            END
        """, (datetime.now().strftime("%Y/%m/%d %H:%M"),))
        
        db.commit()

if __name__ == '__main__':
    init_db()  # ایجاد جدول فقط یک بار
    app.run(debug=True)
