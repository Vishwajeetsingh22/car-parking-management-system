from collections import deque

# 1. LINKED LIST IMPLEMENTATION FOR PARKED VEHICLES

class Node:
    def __init__(self, data):
        self.data = data       # dictionary of vehicle details
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    # Insert at end (Vehicle Entry)
    def insert(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return

        temp = self.head
        while temp.next:
            temp = temp.next
        temp.next = new_node

    # Delete by vehicle number
    def delete(self, vno):
        temp = self.head
        prev = None

        while temp:
            if temp.data["Vehicle_Number"] == vno:
                if prev:
                    prev.next = temp.next
                else:
                    self.head = temp.next
                return temp.data    # return deleted record
            prev = temp
            temp = temp.next
        return None

    # Search vehicle
    def search(self, vno):
        temp = self.head
        while temp:
            if temp.data["Vehicle_Number"] == vno:
                return temp.data
            temp = temp.next
        return None

    # Display all vehicles
    def display(self):
        temp = self.head
        if not temp:
            print("No vehicles parked.")
            return

        while temp:
            print(temp.data)
            temp = temp.next

# DATA STRUCTURES


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


#  MAIN PROGRAM


def main():
    while True:
        print("\n========== PARKING MANAGEMENT SYSTEM ==========")
        print("1. Vehicle Entry")
        print("2. Remove Entry")
        print("3. View Parked Vehicles")
        print("4. View Parking Space Left")
        print("5. Billing Rates")
        print("6. Generate Bill")
        print("7. View Removed Vehicles (Stack)")
        print("8. Exit Program")

        ch = input("Choose Option: ")

    
        # 1. VEHICLE ENTRY → INSERT INTO LINKED LIST
    
        if ch == "1":
            record = {}

            # Vehicle Number
            vno = input("Enter Vehicle Number (XXXX-XX-XXXX): ").upper()
            if vehicles.search(vno):
                print("Vehicle already exists!")
                continue

            record["Vehicle_Number"] = vno

            # Type
            while True:
                t = input("Enter Type (A=Bicycle / B=Bike / C=Car): ").lower()
                if t in vehicle_types:
                    vtype = vehicle_types[t]
                    if parking_slots[vtype] > 0:
                        parking_slots[vtype] -= 1
                        record["Vehicle_Type"] = vtype
                        break
                    else:
                        print("No parking left for", vtype)
                else:
                    print("Invalid type.")

            # More details
            record["Vehicle_Name"] = input("Enter Vehicle Name: ")
            record["Owner_Name"] = input("Enter Owner Name: ")
            record["Date"] = input("Enter Date (DD-MM-YYYY): ")
            record["Entry_Time"] = input("Enter Entry Time (HH:MM:SS): ")
            record["Exit_Time"] = "--------"

            vehicles.insert(record)
            print("Vehicle Added Successfully!")

        # 2. REMOVE VEHICLE → POP INTO STACK
       
        elif ch == "2":
            vno = input("Enter Vehicle Number to Remove: ").upper()
            deleted = vehicles.delete(vno)

            if deleted:
                removed_stack.append(deleted)  # PUSH INTO STACK
                parking_slots[deleted["Vehicle_Type"]] += 1
                print("Vehicle Removed & Added to Stack")
            else:
                print("Vehicle not found!")

    
        # 3. DISPLAY ALL VEHICLES (Linked List Traversal)
   
        elif ch == "3":
            print("\n------ PARKED VEHICLES ------")
            vehicles.display()

       
        # 4. PARKING SPACE LEFT
    
        elif ch == "4":
            print("\n------ PARKING SLOTS LEFT ------")
            for t, s in parking_slots.items():
                print(t, ":", s)

    
        # 5. DISPLAY RATES
      
        elif ch == "5":
            print("\n------ RATES ------")
            for t, r in rates.items():
                print(t, ": Rs", r, "/Hour")

     
        # 6. BILLING → ADD REQUEST TO QUEUE
      
        elif ch == "6":
            vno = input("Enter Vehicle Number: ").upper()
            vehicle = vehicles.search(vno)

            if not vehicle:
                print("Vehicle not found!")
                continue

            billing_queue.append(vehicle)      # ENQUEUE
            print("Added to Billing Queue.")

            # Process queue
            while billing_queue:
                v = billing_queue.popleft()    # DEQUEUE
                hours = int(input("Enter Hours Parked: "))

                amount = rates[v["Vehicle_Type"]] * max(1, hours)
                gst = amount * 0.18
                total = amount + gst

                v["Exit_Time"] = input("Enter Exit Time (HH:MM:SS): ")

                print("\n------ BILL ------")
                print("Base:", amount)
                print("GST:", int(gst))
                print("Total:", int(total))

   
        # 7. SHOW STACK (LAST REMOVED VEHICLES)
    
        elif ch == "7":
            print("\n------ REMOVED VEHICLES (STACK ORDER) ------")
            for v in reversed(removed_stack):
                print(v)

      
        # 8. EXIT
  
        elif ch == "8":
            print("Goodbye!")
            break

        else:
            print("Invalid choice!")


main()

