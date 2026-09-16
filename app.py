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


@app.route("/check_status")
def check_status():
  user_id = request.args.get("user_id")
  if not user_id:
    return jsonify({"status": "error"}), 400

  clients = load_db()
  user_data = clients.get(str(user_id), {})
  status = user_data.get("status", "pending")
  return jsonify({"status": status})


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)