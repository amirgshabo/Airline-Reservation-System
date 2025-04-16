import tkinter as tk # Import the Tkinter library to create the GUI
from tkinter import messagebox # For showing popup messages
import json # To save and load booking data
import os # To check if the bookings file exists

# Flight Class to store info about each flight
class Flight:
    def __init__(self, code, destination, date_time):
        self.code = code # Flight code (like LA123)
        self.destination = destination # Where the flight is going
        self.date_time = date_time # When the flight is leaving

    def __str__(self):
        # This helps print the flight info in a readable way
        return f"{self.code}: {self.destination} at {self.date_time}"
    
# Reservation system class to manage all bookings and flights
class ReservationSystem:
    def __init__(self):
        self.flights = [] # List to store all flights
        self.bookings = {} # Dictionary to store user bookings
        self.load_flights() # Load flights into the list
        self.load_bookings() # Load previous bookings if any
    
    def load_flights(self):
        # Here we just add 3 flights manually
        self.flights = [
            Flight("LA123", "Los Angeles", "2025-05-01 10:00"),
            Flight("TX456", "Texas", "2025-05-02 14:30"),
            Flight("NY789", "New York", "2025-05-03 18:00")
        ]
    
    def load_bookings(self):
        # Load bookings from the JSON file if it exists
        if os.path.exists("bookings.json"):
            with open("bookings.json", "r") as f:
                self.bookings = json.load(f)

    def save_bookings(self):
        # Save bookings to the file so we don't lose them
        with open("bookings.json", "w") as f:
            json.dump(self.bookings, f)

    def get_flight(self, code):
        # Find a flight object by its code
        for flight in self.flights:
            if flight.code == code:
                return flight
        return None  # If not found, return nothing

    def book_flight(self, name, code):
        flight = self.get_flight(code)  # Look up the flight
        if name and flight:
            self.bookings[name] = code  # Save the booking
            self.save_bookings()  # Write to file
            return flight  # Return the flight object
        return None  # If something went wrong

    def view_booking(self, name):
        code = self.bookings.get(name)  # Get the flight code
        if code:
            return self.get_flight(code)  # Return the flight object
        return None  # If not booked

    def cancel_booking(self, name):
        if name in self.bookings:
            del self.bookings[name]  # Remove the booking
            self.save_bookings()  # Save changes
            return True
        return False  # Nothing to cancel

#-------------------------------------GUI-------------------------------------------------#

system = ReservationSystem()  # Create system object
window = tk.Tk()  # Create main window
window.title("Shabo Airline")  # Window title
window.geometry("400x500")  # Size of the window

# Create frames for different pages
main_frame = tk.Frame(window) # Main menu frame
booking_frame = tk.Frame(window) # Booking flights frame
view_frame = tk.Frame(window) # Viewing booked flights frame
cancel_frame = tk.Frame(window) # Cancelling bookings frame

# Configure grid layout for frames
for frame in (main_frame, booking_frame, view_frame, cancel_frame): # Loops through all frames
    frame.grid(row=0, column=0, sticky="nsew") # Puts each frame in the same spot, stacked
window.grid_rowconfigure(0, weight=1) # Vertical
window.grid_columnconfigure(0, weight=1) # Horizontal

# Function to switch between frames
def show_frame(frame): # Function changes which page I see
    frame.tkraise() # Brings the chosen frame to the front

# Main Menu UI
tk.Label(main_frame, text="Shabo Airline", font=("Arial", 20)).pack(pady=20) 
tk.Label(main_frame, text="Welcome to Shabo Airline Reservation System", font=("Arial", 12)).pack(pady=10) 
tk.Button(main_frame, text="Book a Flight", command=lambda: show_frame(booking_frame)).pack(pady=10) # This button takes me to the booking page
tk.Button(main_frame, text="View Bookings", command=lambda: show_frame(view_frame)).pack(pady=10) # This button takes me to the view page
tk.Button(main_frame, text="Cancel Booking", command=lambda: show_frame(cancel_frame)).pack(pady=10) # This button takes me to the cancel page

# Booking UI
tk.Label(booking_frame, text="Book a Flight", font=("Arial", 16)).pack(pady=10)
tk.Label(booking_frame, text="Your Name:").pack()
name_entry = tk.Entry(booking_frame)  # Text box for name
name_entry.pack()

tk.Label(booking_frame, text="Flight Code:").pack()
flight_entry = tk.Entry(booking_frame)  # Text box for flight code
flight_entry.pack()

# Function when "Book" is clicked
def handle_booking():
    name = name_entry.get()
    code = flight_entry.get()
    flight = system.book_flight(name, code)
    if flight:
        messagebox.showinfo("Success", f"{name} booked on {flight}")
    else:
        messagebox.showerror("Error", "Invalid name or flight code.")

tk.Button(booking_frame, text="Book", command=handle_booking).pack(pady=5)
tk.Button(booking_frame, text="Back", command=lambda: show_frame(main_frame)).pack()

# View Booking UI
tk.Label(view_frame, text="View Booking", font=("Arial", 16)).pack(pady=10)
tk.Label(view_frame, text="Your Name:").pack()
view_name_entry = tk.Entry(view_frame)  # Text box for name
view_name_entry.pack()

# Function when "View" is clicked
def handle_view():
    name = view_name_entry.get()
    flight = system.view_booking(name)
    if flight:
        messagebox.showinfo("Booking Found", f"{name} is booked on {flight}")
    else:
        messagebox.showerror("Not Found", "No booking found.")

tk.Button(view_frame, text="View", command=handle_view).pack(pady=5)
tk.Button(view_frame, text="Back", command=lambda: show_frame(main_frame)).pack()

# Cancel Booking UI
tk.Label(cancel_frame, text="Cancel Booking", font=("Arial", 16)).pack(pady=10)
tk.Label(cancel_frame, text="Your Name:").pack()
cancel_name_entry = tk.Entry(cancel_frame)  # Text box for name
cancel_name_entry.pack()

# Function when "Cancel Booking" is clicked
def handle_cancel():
    name = cancel_name_entry.get()
    if system.cancel_booking(name):
        messagebox.showinfo("Cancelled", f"Booking for {name} has been cancelled.")
    else:
        messagebox.showerror("Error", "No booking found to cancel.")

tk.Button(cancel_frame, text="Cancel Booking", command=handle_cancel).pack(pady=5)
tk.Button(cancel_frame, text="Back", command=lambda: show_frame(main_frame)).pack()

# Show main menu when app starts
show_frame(main_frame)

# Run the app
window.mainloop()

