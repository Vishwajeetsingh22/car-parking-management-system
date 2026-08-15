# 🚗 Car Parking Management System

A **Car Parking Management System** developed using **Python, Flask, HTML, CSS, SQLite, and Data Structures** to efficiently manage vehicle parking, parking slots, vehicle records, and parking operations.

---

## 📌 Project Overview

The **Car Parking Management System** is designed to simplify and automate parking management.

The system allows users to manage vehicle entry and exit, check parking availability, store vehicle information, and maintain parking records.

The project combines **Python programming, Data Structures, Database Management, and Web Development** concepts to create a practical parking management solution.

---

## 🎯 Objectives

* 🚗 Manage vehicle entry and exit.
* 🅿️ Manage available parking slots.
* 📋 Maintain vehicle parking records.
* 🔍 Search and retrieve parking information.
* 💾 Store parking data using a database.
* 🌐 Provide a web-based interface using Flask.
* ⚡ Reduce manual parking management.
* 🧠 Apply Data Structures concepts to parking operations.

---

## ✨ Features

### 🚘 Vehicle Management

* Add vehicle details.
* Record vehicle entry.
* Record vehicle exit.
* Search vehicle information.
* Maintain parking history.

### 🅿️ Parking Management

* Check parking slot availability.
* Allocate parking slots.
* Release occupied slots.
* Track occupied and available spaces.

### 💾 Database Management

* Store vehicle information.
* Store parking records.
* Maintain parking status.
* Retrieve stored information.

### 🌐 Web Interface

* Flask-based backend.
* HTML-based frontend.
* User-friendly parking management interface.
* Dynamic interaction between frontend and backend.

### 🧠 Data Structures

The project demonstrates the practical use of data structures for managing parking operations and vehicle records.

---

## 🛠️ Technologies Used

| Technology          | Purpose                        |
| ------------------- | ------------------------------ |
| **Python**          | Core application development   |
| **Flask**           | Web application/backend        |
| **HTML**            | Frontend structure             |
| **CSS**             | User interface styling         |
| **SQLite**          | Database management            |
| **Data Structures** | Parking and vehicle management |
| **Git & GitHub**    | Version control                |

---

## 📂 Project Structure

```text
Car-Parking-Management-System/
│
├── app.py
├── Parking_system.py
├── dsa final code.py
├── new parking code.py
├── flaskserver.py
├── fronten.py
├── flaskapi.html
├── index.html
│
├── src/
│   └── park/
│       └── package.xml
│
├── parking.db
├── parking_system.db
│
├── README.md
└── ...
```

---

## 📄 Main Files

| File                  | Description                            |
| --------------------- | -------------------------------------- |
| `app.py`              | Main Flask application                 |
| `Parking_system.py`   | Main parking management logic          |
| `dsa final code.py`   | Data Structures implementation         |
| `new parking code.py` | Parking system implementation          |
| `flaskserver.py`      | Flask server/backend functionality     |
| `fronten.py`          | Frontend-related Python implementation |
| `flaskapi.html`       | Flask API interface                    |
| `index.html`          | Main web page                          |
| `parking.db`          | Parking database                       |
| `parking_system.db`   | Parking system database                |
| `README.md`           | Project documentation                  |

---

# ⚙️ System Workflow

```text
                 Start
                   │
                   ▼
          Open Parking System
                   │
                   ▼
          Enter Vehicle Details
                   │
                   ▼
        Check Parking Availability
                   │
          ┌────────┴────────┐
          │                 │
       Available          Full
          │                 │
          ▼                 ▼
    Allocate Slot     Display Full
          │
          ▼
     Store Vehicle
       Details
          │
          ▼
    Vehicle Parking
          │
          ▼
    Vehicle Exit
          │
          ▼
    Release Parking
         Slot
          │
          ▼
      Update Record
          │
          ▼
         End
```

---

# 🧠 Data Structures

Data Structures concepts are used to efficiently manage parking operations.

Possible operations include:

* Vehicle insertion
* Vehicle deletion
* Searching vehicle records
* Parking slot allocation
* Parking slot release
* Maintaining vehicle information

The project demonstrates how Data Structures can be applied to a real-world parking management problem.

---

# 🗄️ Database

The system uses **SQLite** for storing parking-related information.

### Example information stored

```text
Vehicle Number
Vehicle Type
Owner Details
Parking Slot
Entry Time
Exit Time
Parking Status
```

The database allows parking information to remain available even after restarting the application.

---

# 🌐 Flask Architecture

The web application follows a basic frontend-backend architecture.

```text
        User
         │
         ▼
   HTML Frontend
         │
         ▼
    Flask Server
         │
         ▼
   Python Backend
         │
         ▼
     SQLite DB
         │
         ▼
 Parking Information
```

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Vishwajeetsingh22/car-parking-management-system.git
```

## 2. Navigate to the Project

```bash
cd car-parking-management-system
```

## 3. Create a Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

---

# 📦 Install Dependencies

Install Flask:

```bash
pip install flask
```

If a `requirements.txt` file is available:

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Application

Run the Flask application:

```bash
python app.py
```

If the application uses another Flask entry file, run the corresponding Python file.

After starting the server, open:

```text
http://127.0.0.1:5000/
```

in your browser.

---

# 🖥️ Application

The application provides an interface for managing parking operations.

### Main Operations

```text
1. Vehicle Entry
2. Parking Slot Allocation
3. Vehicle Information
4. Parking Status
5. Vehicle Exit
6. Parking Slot Release
```

---

# 📸 Screenshots

Add your project screenshots here.

### 🏠 Home Page

```markdown
![Home Page](screenshots/home.png)
```

### 🅿️ Parking Management

```markdown
![Parking Management](screenshots/parking.png)
```

### 🚗 Vehicle Entry

```markdown
![Vehicle Entry](screenshots/vehicle-entry.png)
```

### 📊 Parking Status

```markdown
![Parking Status](screenshots/parking-status.png)
```

> Create a `screenshots` folder and upload your screenshots there.

---

# 🔄 Project Workflow

### Step 1 — Vehicle Entry

The user enters vehicle information into the system.

### Step 2 — Check Availability

The system checks whether a parking slot is available.

### Step 3 — Slot Allocation

If a slot is available, the system assigns a parking slot to the vehicle.

### Step 4 — Store Information

Vehicle and parking information is stored in the database.

### Step 5 — Vehicle Exit

When the vehicle leaves, the system records the exit.

### Step 6 — Release Slot

The occupied parking slot becomes available again.

---

# 🔐 Advantages

* Reduces manual parking management.
* Provides faster vehicle record management.
* Maintains organized parking information.
* Makes parking slot tracking easier.
* Provides database-based record storage.
* Demonstrates real-world use of Data Structures.
* Can be extended into a larger smart parking system.

---

# ⚠️ Limitations

The current version is primarily an academic project and may have limitations such as:

* Limited authentication/security.
* Local database usage.
* No real-time IoT sensor integration.
* No online payment system.
* No cloud-based database.
* Limited scalability for large parking facilities.

---

# 🚀 Future Enhancements

The system can be further improved by adding:

### 📱 Mobile Application

Develop an Android/iOS application for users and parking administrators.

### 📍 Real-Time Parking Detection

Integrate IoT sensors to automatically detect whether a parking slot is occupied.

### 💳 Online Payment

Add digital payment functionality for parking fees.

### 📷 Number Plate Recognition

Use **Computer Vision/OCR** to automatically identify vehicle registration numbers.

### ☁️ Cloud Integration

Move the database to a cloud platform for centralized access.

### 🔔 Notifications

Send notifications when:

* Parking slot becomes available.
* Vehicle parking time is about to expire.
* Payment is required.

### 📊 Admin Dashboard

Create an analytics dashboard showing:

* Total vehicles
* Occupied slots
* Available slots
* Daily parking records
* Revenue
* Peak parking hours

---

# 🔮 Future Smart Parking Architecture

```text
             Vehicle
                │
                ▼
        Number Plate Camera
                │
                ▼
          IoT Parking Sensor
                │
                ▼
          Flask Backend
                │
        ┌───────┴────────┐
        │                │
        ▼                ▼
     Database       Admin Dashboard
        │
        ▼
  Parking Analytics
```

---

# 🎓 Academic Concepts Covered

This project demonstrates concepts from:

* Python Programming
* Object-Oriented Programming
* Data Structures
* Database Management Systems
* Web Development
* Flask Framework
* HTML/CSS
* CRUD Operations
* File Handling
* Git & GitHub

---

# 👨‍💻 Author

**Vishwajeet Singh**

**USN:** 25MCAR0219

**JAIN (Deemed-to-be-University)**

MCA Department

**Interests:** Artificial Intelligence | Machine Learning | Python | Software Development

---

# 🔗 GitHub Repository

**Car Parking Management System**

```text
https://github.com/Vishwajeetsingh22/car-parking-management-system
```

---

# 📜 License

This project is developed for **educational and academic purposes**.

---

# ⭐ Acknowledgement

This project was developed as an academic project to demonstrate the practical implementation of **Python, Flask, Data Structures, Database Management, and Web Development** concepts in a real-world **Car Parking Management System**.

---

## ⭐ Project Summary

**Car Parking Management System** is a Python and Flask-based application that manages vehicle parking, slot allocation, vehicle records, and parking operations. The project combines **Data Structures, Database Management, and Web Development** to provide a practical solution for organizing and managing parking facilities.
