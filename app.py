from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)
DB_FILE = "clients.json"

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route("/")
def index():
    return "LoLa Server is running!"

@app.route("/get_user/<user_id>", methods=["GET"])
def get_user(user_id):
    clients = load_db()
    user_data = clients.get(str(user_id))
    
    if not user_data:
        return jsonify({"status": "pending", "lot": 0.01, "name": "Не указано"})
        
    return jsonify(user_data)

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    user_id = str(data.get("user_id"))
    name = data.get("name", "Без имени")
    
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
        
    clients = load_db()
    
    if user_id not in clients:
        clients[user_id] = {
            "status": "pending",
            "lot": 0.01,
            "name": name
        }
        save_db(clients)
        
    return jsonify({"success": True, "status": clients[user_id]["status"]})

@app.route("/update_lot", methods=["POST"])
def update_lot():
    data = request.json
    user_id = str(data.get("user_id"))
    new_lot = data.get("lot")
    
    clients = load_db()
    if user_id in clients:
        clients[user_id]["lot"] = new_lot
        save_db(clients)
        return jsonify({"success": True})
        
    return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
