from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

@app.route("/api/data")
def get_data():
    conn = sqlite3.connect("energy_data.db")
    cur = conn.cursor()
    cur.execute("SELECT region, volume, price FROM auctions")
    rows = [{"region": r[0], "volume": r[1], "price": r[2]} for r in cur.fetchall()]
    conn.close()
    return jsonify(rows)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
