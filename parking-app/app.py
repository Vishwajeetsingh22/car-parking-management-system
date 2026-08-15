from flask import Flask, render_template, request, redirect, url_for, flash
from collections import deque

app = Flask(__name__)
app.secret_key = "change_this_secret_key"

# ============================================================
#                 LINKED LIST IMPLEMENTATION
# ============================================================

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

    def search(self, vno):
        temp = self.head
        while temp:
            if temp.data["Vehicle_Number"] == vno:
                return temp.data
            temp = temp.next
        return None

    def to_list(self):
        data_list = []
        temp = self.head
        while temp:
            data_list.append(temp.data)
            temp = temp.next
        return data_list


# ============================================================
#                    DATA STRUCTURES
# ============================================================

vehicles = LinkedList()          # Linked list for parking database
removed_stack = []               # Stack for removed vehicles
billing_queue = deque()          # Queue for billing requests

parking_slots = {
    "Bicycle": 78,
    "Bike": 100,
    "Car": 250
}

rates = {
    "Bicycle": 20,
    "Bike": 40,
    "Car": 60
}

vehicle_types = {"a": "Bicycle", "b": "Bike", "c": "Car"}

# store last generated bill to show on UI
last_bill = None


# ============================================================
#                        ROUTES
# ============================================================

@app.route("/")
def index():
    global last_bill
    parked = vehicles.to_list()
    removed = list(reversed(removed_stack))
    return render_template(
        "index.html",
        parked=parked,
        removed=removed,
        parking_slots=parking_slots,
        rates=rates,
        last_bill=last_bill
    )


@app.route("/add_vehicle", methods=["POST"])
def add_vehicle():
    vno = request.form.get("vehicle_number", "").upper().strip()
    vtype = request.form.get("vehicle_type", "")
    vname = request.form.get("vehicle_name", "")
    owner = request.form.get("owner_name", "")
    date = request.form.get("date", "")
    entry_time = request.form.get("entry_time", "")

    if not vno:
        flash("Vehicle number is required.", "error")
        return redirect(url_for("index"))

    # Check duplicate
    if vehicles.search(vno):
        flash("Vehicle already exists!", "error")
        return redirect(url_for("index"))

    if vtype not in parking_slots:
        flash("Invalid vehicle type.", "error")
        return redirect(url_for("index"))

    if parking_slots[vtype] <= 0:
        flash(f"No parking left for {vtype}.", "error")
        return redirect(url_for("index"))

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
    flash("Vehicle added successfully!", "success")
    return redirect(url_for("index"))


@app.route("/remove_vehicle", methods=["POST"])
def remove_vehicle():
    vno = request.form.get("remove_vehicle_number", "").upper().strip()

    if not vno:
        flash("Enter a vehicle number to remove.", "error")
        return redirect(url_for("index"))

    removed = vehicles.delete(vno)
    if removed:
        removed_stack.append(removed)
        parking_slots[removed["Vehicle_Type"]] += 1
        flash("Vehicle removed and added to removed stack.", "success")
    else:
        flash("Vehicle not found!", "error")

    return redirect(url_for("index"))


@app.route("/generate_bill", methods=["POST"])
def generate_bill():
    global last_bill

    vno = request.form.get("bill_vehicle_number", "").upper().strip()
    hours_str = request.form.get("hours", "0")
    exit_time = request.form.get("exit_time", "")

    if not vno:
        flash("Enter a vehicle number for billing.", "error")
        return redirect(url_for("index"))

    vehicle = vehicles.search(vno)
    if not vehicle:
        flash("Vehicle not found!", "error")
        return redirect(url_for("index"))

    try:
        hours = int(hours_str)
        if hours <= 0:
            hours = 1
    except ValueError:
        hours = 1

    vtype = vehicle["Vehicle_Type"]
    base = rates[vtype] * hours
    gst = int(base * 0.18)
    total = int(base + gst)

    if exit_time:
        vehicle["Exit_Time"] = exit_time

    last_bill = {
        "Vehicle_Number": vno,
        "Vehicle_Type": vtype,
        "Owner_Name": vehicle["Owner_Name"],
        "Hours": hours,
        "Base": base,
        "GST": gst,
        "Total": total,
        "Exit_Time": vehicle.get("Exit_Time", exit_time)
    }

    flash("Bill generated successfully!", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
