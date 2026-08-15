from flask import Flask, request, jsonify, send_from_directory
from collections import deque
import csv
import io

# -------------------------------
# LINKED LIST IMPLEMENTATION
# -------------------------------

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        temp = self.head
        while temp.next:
            temp = temp.next
        temp.next = new_node

    def search(self, vno):
        temp = self.head
        while temp:
            if temp.data["Vehicle_Number"] == vno:
                return temp.data
            temp = temp.next
        return None

    def delete(self, vno):
        temp = self.head
        prev = None
        while temp:
            if temp.data["Vehicle_Number"] == vno:
                if prev:
                    prev.next = temp.next
                else:
                    self.head = temp.next
                return temp.data
            prev = temp
            temp = temp.next
        return None

    def get_all(self):
        data_list = []
        temp = self.head
        while temp:
            data_list.append(temp.data)
            temp = temp.next
        return data_list

    def count_by_type(self):
        counts = {"Bicycle": 0, "Bike": 0, "Car": 0}
        temp = self.head
        while temp:
            vtype = temp.data.get("Vehicle_Type")
            if vtype in counts:
                counts[vtype] += 1
            temp = temp.next
        return counts


# ----------------------------
# DATA STRUCTURES (SAME LOGIC AS CONSOLE VERSION)
# ----------------------------

vehicles = LinkedList()
removed_stack = []
billing_queue = deque()

parking_slots = {"Bicycle": 78, "Bike": 100, "Car": 250}
rates = {"Bicycle": 20, "Bike": 40, "Car": 60}

# ----------------------------
# FLASK APP
# ----------------------------

app = Flask(__name__)


# Serve the HTML file
@app.route("/")
def index():
    return send_from_directory(".", "index.html")


# GET all vehicles / POST add vehicle
@app.route("/api/vehicles", methods=["GET", "POST"])
def api_vehicles():
    if request.method == "GET":
        return jsonify(vehicles.get_all())

    # POST: Add vehicle
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON body"}), 400

    vno = data.get("Vehicle_Number", "").upper()
    vtype = data.get("Vehicle_Type")
    vname = data.get("Vehicle_Name", "")
    owner = data.get("Owner_Name", "")
    date = data.get("Date", "")
    entry_time = data.get("Entry_Time", "")

    if not vno or not vtype:
        return jsonify({"error": "Vehicle_Number and Vehicle_Type are required"}), 400

    if vehicles.search(vno):
        return jsonify({"error": "Vehicle already exists"}), 400

    if vtype not in parking_slots:
        return jsonify({"error": "Invalid Vehicle_Type"}), 400

    if parking_slots[vtype] <= 0:
        return jsonify({"error": f"No parking slots left for {vtype}"}), 400

    parking_slots[vtype] -= 1

    record = {
        "Vehicle_Number": vno,
        "Vehicle_Type": vtype,
        "Vehicle_Name": vname,
        "Owner_Name": owner,
        "Date": date,
        "Entry_Time": entry_time,
        "Exit_Time": "--------"
    }

    vehicles.insert(record)
    return jsonify({"message": "Vehicle added", "vehicle": record}), 201


# DELETE a vehicle by vehicle number
@app.route("/api/vehicles/<vno>", methods=["DELETE"])
def api_delete_vehicle(vno):
    vno = vno.upper()
    deleted = vehicles.delete(vno)
    if not deleted:
        return jsonify({"error": "Vehicle not found"}), 404

    removed_stack.append(deleted)
    parking_slots[deleted["Vehicle_Type"]] += 1
    return jsonify({"message": "Vehicle removed", "vehicle": deleted})


# GET parking slots + current parked count
@app.route("/api/slots", methods=["GET"])
def api_slots():
    counts = vehicles.count_by_type()
    return jsonify({
        "slots_left": parking_slots,
        "parked_count": counts,
        "total_parked": sum(counts.values())
    })


# POST generate bill
@app.route("/api/bill", methods=["POST"])
def api_bill():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON body"}), 400

    vno = data.get("Vehicle_Number", "").upper()
    hours = data.get("Hours")
    exit_time = data.get("Exit_Time", "")

    vehicle = vehicles.search(vno)
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404

    try:
        hours = int(hours)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid Hours"}), 400

    amount = rates[vehicle["Vehicle_Type"]] * max(1, hours)
    gst = int(amount * 0.18)
    total = amount + gst

    vehicle["Exit_Time"] = exit_time

    return jsonify({
        "message": "Bill generated",
        "vehicle": vehicle,
        "base_amount": amount,
        "gst": gst,
        "total": total
    })


# GET removed vehicles (stack)
@app.route("/api/removed", methods=["GET"])
def api_removed():
    # last removed first
    return jsonify(list(reversed(removed_stack)))


# Export to CSV (download from backend)
@app.route("/api/export", methods=["GET"])
def api_export():
    output = io.StringIO()
    writer = csv.writer(output)

    cols = ["Vehicle_Number", "Vehicle_Type", "Vehicle_Name",
            "Owner_Name", "Date", "Entry_Time", "Exit_Time"]
    writer.writerow(cols)

    for v in vehicles.get_all():
        writer.writerow([v[c] for c in cols])

    output.seek(0)
    return app.response_class(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=parked_vehicles.csv"
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
