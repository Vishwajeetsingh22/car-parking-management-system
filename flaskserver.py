from flask import Flask, request, jsonify
from flask_cors import CORS   # allow frontend to access API

app = Flask(__name__)
CORS(app)   # enable API access from browser

# Example API: Save vehicle data
@app.route('/api/add_vehicle', methods=['POST'])
def add_vehicle():
    data = request.get_json()

    vehicle_no = data.get("vehicle_no")
    vehicle_type = data.get("vehicle_type")
    owner_name = data.get("owner_name")

    # You can save this data in file / database here

    return jsonify({
        "status": "success",
        "message": "Vehicle added successfully!",
        "data": data
    })

# Example API: Get parking status
@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({
        "cars_available": 40,
        "bikes_available": 20
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)
