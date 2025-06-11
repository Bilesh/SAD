from flask import Flask, jsonify, request

app = Flask(__name__)

# Default signal timings (in seconds)
signal_timings = {
    "red": 4,
    "yellow": 2,
    "green": 6
}

@app.route("/api/getTimings", methods=["GET"])
def get_timings():
    """Returns current traffic signal timings"""
    return jsonify(signal_timings)

@app.route("/api/updateTimings", methods=["POST"])
def update_timings():
    """Update traffic signal durations"""
    data = request.json
    signal_timings.update(data)
    return jsonify({"message": "Updated successfully!", "newTimings": signal_timings})

@app.route("/api/pedestrian", methods=["POST"])
def pedestrian_request():
    """Handle pedestrian crossing request"""
    signal_timings["red"] = 6  # Extend red duration for crossing
    return jsonify({"message": "Pedestrian crossing activated!", "red_duration": signal_timings["red"]})

@app.route("/api/emergency", methods=["POST"])
def emergency_override():
    """Override traffic signals for emergency vehicles"""
    signal_timings["green"] = 8  # Extend green duration for priority passage
    return jsonify({"message": "Emergency override activated!", "green_duration": signal_timings["green"]})

if __name__ == "__main__":
    app.run(debug=True)
