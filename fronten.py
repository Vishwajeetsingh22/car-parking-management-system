import customtkinter as ctk
from tkinter import messagebox, filedialog
from tkinter import PhotoImage
import sqlite3
from collections import deque
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

# Optional: voice input
try:
    import speech_recognition as sr
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False


# ================== DATA STRUCTURES (LinkedList, Stack, Queue) ================== #

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

    def get_all(self):
        temp = self.head
        res = []
        while temp:
            res.append(temp.data)
            temp = temp.next
        return res


vehicles_ll = LinkedList()      # Linked list for active vehicles
removed_stack = []              # Stack of removed vehicles
billing_queue = deque()         # Queue for billing

parking_slots = {"Bicycle": 78, "Bike": 100, "Car": 250}
rates = {"Bicycle": 20, "Bike": 40, "Car": 60}


# ================== SQLITE DATABASE SETUP ================== #

DB_NAME = "parking_system.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_number TEXT UNIQUE,
            vehicle_type TEXT,
            vehicle_name TEXT,
            owner_name TEXT,
            entry_time TEXT,
            exit_time TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

def db_add_vehicle(record):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO vehicles 
        (vehicle_number, vehicle_type, vehicle_name, owner_name, entry_time, exit_time, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        record["Vehicle_Number"],
        record["Vehicle_Type"],
        record["Vehicle_Name"],
        record["Owner_Name"],
        record["Entry_Time"],
        record["Exit_Time"],
        "Parked"
    ))
    conn.commit()
    conn.close()

def db_set_exit(vehicle_number, exit_time):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        UPDATE vehicles
        SET exit_time = ?, status = 'Exited'
        WHERE vehicle_number = ?
    """, (exit_time, vehicle_number))
    conn.commit()
    conn.close()

def db_get_parked():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT vehicle_number, vehicle_type, vehicle_name, owner_name, entry_time FROM vehicles WHERE status='Parked'")
    rows = c.fetchall()
    conn.close()
    return rows

def db_get_exited():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT vehicle_number, vehicle_type, vehicle_name, owner_name, entry_time, exit_time FROM vehicles WHERE status='Exited'")
    rows = c.fetchall()
    conn.close()
    return rows

# ================== BILLING + PDF ================== #

def calculate_bill(entry_time_str, exit_time_str, vtype):
    fmt = "%Y-%m-%d %H:%M:%S"
    entry_dt = datetime.strptime(entry_time_str, fmt)
    exit_dt = datetime.strptime(exit_time_str, fmt)

    diff = exit_dt - entry_dt
    hours = diff.total_seconds() / 3600.0
    hours_rounded = max(1, int(hours + 0.99))  # round up at least 1 hour

    amount = rates[vtype] * hours_rounded
    gst = amount * 0.18
    total = amount + gst
    return hours_rounded, amount, int(gst), int(total)


def generate_pdf_bill(filename, bill_info):
    """
    bill_info: dict with keys:
        vehicle_number, vehicle_type, owner_name, entry_time, exit_time,
        hours, amount, gst, total
    """
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    c.setTitle("Parking Bill")
    c.setFont("Helvetica-Bold", 20)
    c.drawString(200, height - 80, "Parking Bill")

    c.setFont("Helvetica", 12)
    y = height - 140
    for key, label in [
        ("vehicle_number", "Vehicle Number"),
        ("vehicle_type", "Vehicle Type"),
        ("owner_name", "Owner Name"),
        ("entry_time", "Entry Time"),
        ("exit_time", "Exit Time"),
        ("hours", "Hours Parked"),
        ("amount", "Base Amount (Rs)"),
        ("gst", "GST (Rs)"),
        ("total", "Total (Rs)")
    ]:
        c.drawString(80, y, f"{label}: {bill_info[key]}")
        y -= 20

    c.showPage()
    c.save()


# ================== GUI (CustomTkinter) ================== #

ctk.set_appearance_mode("dark")  # Dark mode
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Professional Parking Management System")
app.geometry("1100x650")

# Load icons (if files missing, ignore)
car_icon = bike_icon = bicycle_icon = None
try:
    car_icon = PhotoImage(file="car.png")
except:
    pass
try:
    bike_icon = PhotoImage(file="bike.png")
except:
    pass
try:
    bicycle_icon = PhotoImage(file="bicycle.png")
except:
    pass

# ---------- Top Title ---------- #
title_label = ctk.CTkLabel(
    app, text="Parking Management System",
    font=ctk.CTkFont(size=24, weight="bold")
)
title_label.pack(pady=10)

# ---------- Main Frames ---------- #
main_frame = ctk.CTkFrame(app)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

left_frame = ctk.CTkFrame(main_frame)
left_frame.pack(side="left", fill="y", padx=10, pady=10)

right_frame = ctk.CTkFrame(main_frame)
right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# ---------- Left Panel: Form + Buttons ---------- #

form_title = ctk.CTkLabel(left_frame, text="Vehicle Details", font=ctk.CTkFont(size=18, weight="bold"))
form_title.pack(pady=10)

vno_entry = ctk.CTkEntry(left_frame, placeholder_text="Vehicle Number (e.g. MH12-AB-1234)", width=220)
vno_entry.pack(pady=5)

vtype_option = ctk.CTkComboBox(left_frame, values=["Bicycle", "Bike", "Car"], width=220)
vtype_option.set("Car")
vtype_option.pack(pady=5)

vname_entry = ctk.CTkEntry(left_frame, placeholder_text="Vehicle Name / Model", width=220)
vname_entry.pack(pady=5)

owner_entry = ctk.CTkEntry(left_frame, placeholder_text="Owner Name", width=220)
owner_entry.pack(pady=5)

# Parking info label
slots_label = ctk.CTkLabel(left_frame, text="", font=ctk.CTkFont(size=12))
slots_label.pack(pady=5)


def update_slots_label():
    txt = "Slots Left → "
    txt += f"Bicycle: {parking_slots['Bicycle']} | "
    txt += f"Bike: {parking_slots['Bike']} | "
    txt += f"Car: {parking_slots['Car']}"
    slots_label.configure(text=txt)


# ---------- Voice Input Button ---------- #

def voice_fill_vno():
    if not VOICE_AVAILABLE:
        messagebox.showerror("Error", "SpeechRecognition or PyAudio not installed.")
        return
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Voice Input", "Speak vehicle number clearly...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        vno_entry.delete(0, "end")
        vno_entry.insert(0, text.upper().replace(" ", ""))
        messagebox.showinfo("Recognized", f"Detected: {text}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not recognize speech: {e}")


voice_btn = ctk.CTkButton(left_frame, text="🎤 Voice Input (Vehicle No.)", command=voice_fill_vno, width=220)
voice_btn.pack(pady=5)

# ---------- Buttons ---------- #

def add_vehicle():
    vno = vno_entry.get().strip().upper()
    vtype = vtype_option.get()
    vname = vname_entry.get().strip()
    owner = owner_entry.get().strip()

    if not vno or not vname or not owner:
        messagebox.showerror("Error", "Please fill all fields.")
        return

    if vtype not in parking_slots:
        messagebox.showerror("Error", "Invalid vehicle type selected.")
        return

    if parking_slots[vtype] <= 0:
        messagebox.showerror("Error", f"No slots left for {vtype}.")
        return

    if vehicles_ll.search(vno):
        messagebox.showerror("Error", "Vehicle already parked (LinkedList).")
        return

    # Create record
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record = {
        "Vehicle_Number": vno,
        "Vehicle_Type": vtype,
        "Vehicle_Name": vname,
        "Owner_Name": owner,
        "Entry_Time": now,
        "Exit_Time": "------"
    }

    # LinkedList + DB + Slots
    vehicles_ll.insert(record)
    parking_slots[vtype] -= 1
    try:
        db_add_vehicle(record)
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Vehicle already exists in DB.")
        return

    update_slots_label()
    refresh_lists()
    messagebox.showinfo("Success", f"Vehicle {vno} added at {now}.")


def remove_vehicle():
    vno = vno_entry.get().strip().upper()
    if not vno:
        messagebox.showerror("Error", "Enter Vehicle Number to remove.")
        return

    deleted = vehicles_ll.delete(vno)
    if not deleted:
        messagebox.showerror("Error", "Vehicle not found in LinkedList.")
        return

    parking_slots[deleted["Vehicle_Type"]] += 1
    removed_stack.append(deleted)

    # Set exit time in DB
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db_set_exit(vno, now)

    update_slots_label()
    refresh_lists()
    messagebox.showinfo("Removed", f"Vehicle {vno} removed at {now} and pushed to stack.")


def generate_bill():
    vno = vno_entry.get().strip().upper()
    if not vno:
        messagebox.showerror("Error", "Enter Vehicle Number to bill.")
        return

    vehicle = vehicles_ll.search(vno)
    if not vehicle:
        messagebox.showerror("Error", "Vehicle not found in active list.")
        return

    entry_time_str = vehicle["Entry_Time"]
    exit_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    vehicle["Exit_Time"] = exit_time_str

    # Update in DB as well
    db_set_exit(vno, exit_time_str)

    hours, amount, gst, total = calculate_bill(entry_time_str, exit_time_str, vehicle["Vehicle_Type"])

    info = (
        f"Vehicle: {vno}\n"
        f"Type: {vehicle['Vehicle_Type']}\n"
        f"Owner: {vehicle['Owner_Name']}\n"
        f"Entry: {entry_time_str}\n"
        f"Exit: {exit_time_str}\n"
        f"Hours: {hours}\n"
        f"Base: Rs {amount}\n"
        f"GST: Rs {gst}\n"
        f"Total: Rs {total}"
    )

    # Ask to save PDF
    if messagebox.askyesno("Bill Generated", info + "\n\nSave as PDF?"):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            initialfile=f"Bill_{vno}.pdf"
        )
        if file_path:
            bill_info = {
                "vehicle_number": vno,
                "vehicle_type": vehicle["Vehicle_Type"],
                "owner_name": vehicle["Owner_Name"],
                "entry_time": entry_time_str,
                "exit_time": exit_time_str,
                "hours": str(hours),
                "amount": str(amount),
                "gst": str(gst),
                "total": str(total)
            }
            generate_pdf_bill(file_path, bill_info)
            messagebox.showinfo("Saved", f"PDF saved at:\n{file_path}")

    # Also remove from LinkedList and push to stack (as exited)
    vehicles_ll.delete(vno)
    removed_stack.append(vehicle)
    parking_slots[vehicle["Vehicle_Type"]] += 1
    update_slots_label()
    refresh_lists()


add_btn = ctk.CTkButton(left_frame, text="➕ Add Vehicle", command=add_vehicle, width=220)
add_btn.pack(pady=5)

remove_btn = ctk.CTkButton(left_frame, text="➖ Remove Vehicle", command=remove_vehicle, width=220)
remove_btn.pack(pady=5)

bill_btn = ctk.CTkButton(left_frame, text="🧾 Generate Bill", command=generate_bill, width=220)
bill_btn.pack(pady=5)


# ---------- Right Panel: Lists + Icons ---------- #

top_right = ctk.CTkFrame(right_frame)
top_right.pack(fill="both", expand=True, padx=10, pady=10)

bottom_right = ctk.CTkFrame(right_frame)
bottom_right.pack(fill="x", padx=10, pady=10)

parked_label = ctk.CTkLabel(top_right, text="Parked Vehicles", font=ctk.CTkFont(size=16, weight="bold"))
parked_label.pack(pady=5)

parked_listbox = ctk.CTkTextbox(top_right, height=10, width=600)
parked_listbox.pack(pady=5)

removed_label = ctk.CTkLabel(top_right, text="Removed Vehicles (Stack - Last on Top)", font=ctk.CTkFont(size=16, weight="bold"))
removed_label.pack(pady=5)

removed_listbox = ctk.CTkTextbox(top_right, height=8, width=600)
removed_listbox.pack(pady=5)


def refresh_lists():
    # Parked (from DB)
    parked_listbox.configure(state="normal")
    parked_listbox.delete("1.0", "end")
    rows = db_get_parked()
    for r in rows:
        vno, vtype, vname, owner, entry = r
        parked_listbox.insert("end", f"{vno} | {vtype} | {vname} | {owner} | {entry}\n")
    parked_listbox.configure(state="disabled")

    # Removed (from stack)
    removed_listbox.configure(state="normal")
    removed_listbox.delete("1.0", "end")
    for v in reversed(removed_stack):
        removed_listbox.insert("end", f"{v['Vehicle_Number']} | {v['Vehicle_Type']} | {v['Owner_Name']}\n")
    removed_listbox.configure(state="disabled")


# Bottom right: icons + status
icon_frame = ctk.CTkFrame(bottom_right)
icon_frame.pack(pady=5)

if bicycle_icon:
    ctk.CTkLabel(icon_frame, image=bicycle_icon, text="").grid(row=0, column=0, padx=10)
if bike_icon:
    ctk.CTkLabel(icon_frame, image=bike_icon, text="").grid(row=0, column=1, padx=10)
if car_icon:
    ctk.CTkLabel(icon_frame, image=car_icon, text="").grid(row=0, column=2, padx=10)

status_label = ctk.CTkLabel(bottom_right, text="Ready.", font=ctk.CTkFont(size=12))
status_label.pack(pady=5)


def periodic_status_update():
    status_label.configure(text=f"Total Parked: {len(db_get_parked())} | Removed Stack Size: {len(removed_stack)}")
    app.after(3000, periodic_status_update)


# ================== MAIN ================== #

if __name__ == "__main__":
    init_db()
    update_slots_label()
    refresh_lists()
    periodic_status_update()
    app.mainloop()
