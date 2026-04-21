from flask import Flask, request, jsonify
import psycopg2
import datetime
import os
from dotenv import load_dotenv
load_dotenv() # 讀取 .env 檔案中的環境變數
app = Flask(__name__)

# 你的實驗室電腦資料庫連線字串
postgresql_url = os.getenv('DATABASE_URL')

# 建立一個共用的資料庫連線與寫入函式，減少重複程式碼
def insert_data(sql, params):
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(postgresql_url)
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        return True, "寫入成功"
    except Exception as e:
        print(f"資料庫寫入錯誤: {e}")
        return False, str(e)
    finally:
        if cur: cur.close()
        if conn: conn.close()

# ---------------------------------------------------------
# 端點 1：接收環境感測器資料 (溫溼度、光照)
# ---------------------------------------------------------
@app.route('/upload/environment', methods=['POST'])
def upload_environment():
    data = request.get_json()
    if not data: return jsonify({"error": "無效的 JSON 資料"}), 400

    # 提取資料 (對應 environment_sensor_data)
    temp = data.get('temperature')
    hum = data.get('humidity')
    light = data.get('light_level')

    sql = "INSERT INTO environment_sensor_data (temperature, humidity, light_level) VALUES (%s, %s, %s)"
    success, msg = insert_data(sql, (temp, hum, light))
    
    if success:
        return jsonify({"status": "success", "message": "環境資料已寫入"}), 200
    else:
        return jsonify({"status": "error", "message": msg}), 500

# ---------------------------------------------------------
# 端點 2：接收毫米波雷達資料 (呼吸、心跳、狀態)
# ---------------------------------------------------------
@app.route('/upload/mmwave', methods=['POST'])
def upload_mmwave():
    data = request.get_json()
    if not data: return jsonify({"error": "無效的 JSON 資料"}), 400

    # 提取資料 (對應 mmwave_sensor_data)
    breath_rate = data.get('breath_rate')
    heart_rate = data.get('heart_rate')
    breath_phase = data.get('breath_phase')
    heart_phase = data.get('heart_phase')
    status_code = data.get('status_code') # 此欄位為 NOT NULL，必須有值

    if status_code is None:
        return jsonify({"error": "缺少必要欄位 status_code"}), 400

    sql = """
        INSERT INTO mmwave_sensor_data 
        (breath_rate, heart_rate, breath_phase, heart_phase, status_code) 
        VALUES (%s, %s, %s, %s, %s)
    """
    success, msg = insert_data(sql, (breath_rate, heart_rate, breath_phase, heart_phase, status_code))
    
    if success:
        return jsonify({"status": "success", "message": "毫米波資料已寫入"}), 200
    else:
        return jsonify({"status": "error", "message": msg}), 500

# ---------------------------------------------------------
# 端點 3：接收智慧插座資料 (電壓、電流、功率)
# ---------------------------------------------------------
@app.route('/upload/smart_plug', methods=['POST'])
def upload_smart_plug():
    data = request.get_json()
    if not data: return jsonify({"error": "無效的 JSON 資料"}), 400

    # 提取資料 (對應 smart_plug_logs)
    log_time = data.get('log_time')
    device_name = data.get('device_name')
    status = data.get('status')
    power_w = data.get('power_w')
    voltage_v = data.get('voltage_v')
    current_ma = data.get('current_ma')
    daily_energy_kwh = data.get('daily_energy_kwh')
    
    if not device_name or not status:
        return jsonify({"error": "缺少必要欄位 device_name 或 status"}), 400

    # 由於 smart_plug_logs 沒有設定 DEFAULT CURRENT_TIMESTAMP，我們由後端補上當下時間
    log_time = datetime.datetime.now()

    sql = """
        INSERT INTO smart_plug_logs 
        (log_time, device_name, status, power_w, voltage_v, current_ma, daily_energy_kwh) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    success, msg = insert_data(sql, (log_time, device_name, status, power_w, voltage_v, current_ma, daily_energy_kwh))
    
    if success:
        return jsonify({"status": "success", "message": "智慧插座資料已寫入"}), 200
    else:
        return jsonify({"status": "error", "message": msg}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)