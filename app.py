from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import threading
import time

app = Flask(__name__, static_folder='static')
CORS(app)

traffic_state = {
    "signal": "Red",
    "auto_mode": True
}

def auto_signal_changer():
    sequence = ["Red", "Green", "Yellow"]
    index = 0
    while True:
        time.sleep(5)  # change signal every 5 seconds
        if traffic_state["auto_mode"]:
            traffic_state["signal"] = sequence[index]
            index = (index + 1) % 3

# Start background thread
threading.Thread(target=auto_signal_changer, daemon=True).start()

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/get-signal', methods=['GET'])
def get_signal():
    return jsonify(traffic_state)

@app.route('/set-signal', methods=['POST'])
def set_signal():
    data = request.json
    signal = data.get("signal")
    if signal in ["Red", "Yellow", "Green"]:
        traffic_state["signal"] = signal
        traffic_state["auto_mode"] = False  # pause auto if manually changed
        return jsonify({"status": "manual override", "signal": traffic_state["signal"]})
    return jsonify({"status": "error", "message": "Invalid signal"}), 400

@app.route('/toggle-auto', methods=['POST'])
def toggle_auto():
    traffic_state["auto_mode"] = not traffic_state["auto_mode"]
    return jsonify({"auto_mode": traffic_state["auto_mode"]})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
