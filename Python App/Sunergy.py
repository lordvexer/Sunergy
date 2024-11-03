from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/help')
def help_page():
    return render_template('help.html')

@app.route('/workroute')
def workroute():
    return render_template('workroute.html')

@app.route('/calculate', methods=['POST'])
def calculate():
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
    # roi_message = f"بازگشت سرمایه در مدت ۴ سال: {total_income:,.0f} تومان"  # فرمت‌دهی عددی
    roi_message = f"بازگشت سرمایه در مدت ۴ سال" 

    return jsonify({
        'ground_space': ground_space,
        'rooftop_space': rooftop_space,
        'construction_cost': construction_cost,
        'roi_message': roi_message
    })

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


if __name__ == '__main__':
    app.run(debug=True)
