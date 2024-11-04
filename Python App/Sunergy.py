from flask import Flask, render_template, request, jsonify, g, session, redirect
from datetime import datetime
import pyodbc
import random
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# تنظیمات اتصال به SQL Server
DATABASE_CONFIG = {
    'server': 'SHAFAFTVEDC-SRV',
    'database': 'sunergy',
    'username': 'sunergy',
    'password': 'Sun@2412%$#'
}

# Store active sessions
active_users = set()  # This will store user sessions

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

# بستن اتصال دیتابیس پس از پایان هر درخواست
@app.teardown_appcontext
def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    db = get_db()
    cursor = db.cursor()
    
    # ایجاد شناسه جلسه جدید
    session['user_id'] = request.remote_addr  # یا یک شناسه یکتا دیگر
    
    # اضافه کردن کاربر به لیست کاربران آنلاین
    active_users.add(session['user_id'])

    try:
        # افزایش تعداد بازدیدها و به‌روزرسانی تاریخ
        cursor.execute("UPDATE stats SET visits = visits + 1, last_update = ?", 
                       (datetime.now().strftime("%Y/%m/%d %H:%M"),))
        db.commit()
        
        # دریافت تعداد بازدیدها و تاریخ آخرین به‌روزرسانی
        cursor.execute("SELECT visits, last_update FROM stats")
        stats = cursor.fetchone()
        visits = stats[0]
        last_update = stats[1]
        
        # تعداد کاربران آنلاین را بر اساس طول active_users محاسبه کنید
        users_online = len(active_users)
        
        # انتخاب تصادفی یک نقل‌قول
        quote, author = random.choice(quotes)
        
        return render_template('index.html', visits=visits, users_online=users_online, last_update=last_update, quote=quote, author=author)
    
    except Exception as e:
        return jsonify({"error": "Error updating stats."}), 500

@app.route('/logout')
def logout():
    user_id = session.pop('user_id', None)
    if user_id in active_users:
        active_users.remove(user_id)
    return redirect('/')  # یا صفحه‌ای دیگر

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        capacity = float(request.form['capacity'])
        
        # محاسبات
        if capacity <= 200:
            ground_space = capacity * 10  # فضای زمین به متر مربع
        else:
            ground_space = capacity * 15  # فضای زمین برای ظرفیت‌های بالای 200 کیلووات

        rooftop_space = ground_space * 0.85  # فضای سقف به متر مربع (85% از فضای زمین)
        construction_cost = capacity * 26000000  # هزینه ساخت به تومان (260 میلیون تومان به ازای هر کیلووات)
        
        # محاسبه ROI
        annual_income = capacity * 5000000  # فرض بر این است که درآمد سالانه به ازای هر کیلووات ۵ میلیون تومان باشد
        total_income = annual_income * 4  # درآمد ۴ ساله
        roi_message = f"بازگشت سرمایه در مدت ۴ سال "
        
        return jsonify({
            'ground_space': ground_space,
            'rooftop_space': rooftop_space,
            'construction_cost': construction_cost,
            'roi_message': roi_message
        })

    except ValueError:
        return jsonify({"error": "Invalid capacity value."}), 400
    

# بارگذاری نقل قول‌ها از فایل متنی
def load_quotes():
    with open('quotes.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        quotes = [tuple(line.strip().split(' - ')) for line in lines]
    return quotes

quotes = load_quotes()



@app.route('/calculate_capacity')
def calculate_capacity():
    try:
        # دریافت مقدار انرژی از درخواست
        energy = float(request.args.get('energy', 0))
        # محاسبه ظرفیت نیروگاه
        capacity = (energy * 0.05) / 1750
        return jsonify({"capacity": round(capacity, 2)})
    except (TypeError, ValueError):
        return jsonify({"error": "مقدار ورودی نامعتبر است"}), 400

@app.route('/help')
def help_page():
    return render_template('help.html')

@app.route('/workroute')
def workroute():
    return render_template('workroute.html')

if __name__ == '__main__':
    app.run(debug=True)
