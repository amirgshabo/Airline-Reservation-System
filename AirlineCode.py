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
        # Load flights from file if it exists
        if os.path.exists("flights.json"):
            with open("flights.json", "r") as f:
                flights_data = json.load(f)
                self.flights = [Flight(f["code"], f["destination"], f["date_time"]) for f in flights_data]
        else:
            # If no file, start with 3 default flights
            self.flights = [
                Flight("LA123", "Los Angeles", "2025-05-01 10:00"),
                Flight("TX456", "Texas", "2025-05-02 14:30"),
                Flight("NY789", "New York", "2025-05-03 18:00")
            ]
            self.save_flights() # Save them to file
   
    def save_flights(self):
        # Save all flights to a file so they don't get lost after closing
        with open("flights.json", "w") as f:
            flights_data = [{"code": flight.code, "destination": flight.destination, "date_time": flight.date_time} for flight in self.flights]
            json.dump(flights_data, f)
   
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
        return None # If not found, return nothing

    def book_flight(self, name, code):
        flight = self.get_flight(code) # Look up the flight
        if name and flight:
            self.bookings[name] = code # Save the booking
            self.save_bookings() # Write to file
            return flight # Return the flight object
        return None # If something went wrong

    def view_booking(self, name):
        code = self.bookings.get(name) # Get the flight code
        if code:
            return self.get_flight(code) # Return the flight object
        return None # If not booked

    def cancel_booking(self, name):
        if name in self.bookings:
            del self.bookings[name] # Remove the booking
            self.save_bookings() # Save changes
            return True
        return False # Nothing to cancel
   
    def delete_flight(self, code):
        # Check if flight exists
        flight = self.get_flight(code)
        if not flight:
            return False # Flight not found
        # Check if any bookings exist for this flight
        for name, booked_code in self.bookings.items():
            if booked_code == code:
                return False # Can't delete, flight is booked
        # Remove the flight
        self.flights = [f for f in self.flights if f.code != code]
        self.save_flights()
        return True

# Base frame class for common setup
class BaseFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=0, sticky="nsew") # Put frame in the same spot
        parent.grid_rowconfigure(0, weight=1) # Vertical stretch
        parent.grid_columnconfigure(0, weight=1) # Horizontal stretch

# Login frame class
class LoginFrame(BaseFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app # Reference to FlightApp for navigation


        tk.Label(self, text="Login Page", font=("Arial", 20)).pack(pady=20) # Title
        tk.Label(self, text="Select User Type:").pack() # Ask user type


        # Buttons for selecting user type
        tk.Button(self, text="User", width=15, command=self.handle_user_login).pack(pady=10)
        tk.Button(self, text="Admin", width=15, command=self.handle_admin_login).pack(pady=5)


    def handle_user_login(self):
        # Create popup for user name input
        def submit_name():
            user_name = user_name_entry.get()
            if user_name:
                messagebox.showinfo("Login Successful", f"Welcome, {user_name}!")
                self.app.show_frame(self.app.main_frame) # Go to main menu
                name_window.destroy()
            else:
                messagebox.showerror("Error", "Please enter your name.")


        name_window = tk.Toplevel(self.master) # Create popup window
        name_window.title("Enter Name") # Window title
        name_window.geometry("300x150") # Window size


        tk.Label(name_window, text="Please enter your name:").pack(pady=10)
        user_name_entry = tk.Entry(name_window)
        user_name_entry.pack(pady=5)


        tk.Button(name_window, text="Submit", command=submit_name).pack(pady=10)

    def handle_admin_login(self):
        # Create popup for admin password
        def submit_password():
            entered = password_entry.get()
            if entered == "2025": # Correct password
                messagebox.showinfo("Login Successful", "Welcome, Admin!")
                password_window.destroy() # Close popup
                self.app.show_frame(self.app.admin_frame) # Go to admin menu
            else:
                messagebox.showerror("Error", "Incorrect password.")
       
        password_window = tk.Toplevel(self.master) # Small window on top
        password_window.title("Admin Login") # Title
        password_window.geometry("300x150") # Size


        tk.Label(password_window, text="Enter Admin Password:").pack(pady=10) # Label
        password_entry = tk.Entry(password_window, show="*") # Hide text
        password_entry.pack(pady=5) # Entry box


        tk.Button(password_window, text="Submit", command=submit_password).pack(pady=10)

# Main menu frame class
class MainFrame(BaseFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app # Reference to FlightApp

        tk.Label(self, text="Shabo Airline", font=("Arial", 20)).pack(pady=20)
        tk.Label(self, text="Welcome to Shabo Airline Reservation System", font=("Arial", 12)).pack(pady=10)
        tk.Button(self, text="Book a Flight", command=lambda: self.app.show_frame(self.app.booking_frame)).pack(pady=10) # This button takes me to booking page
        tk.Button(self, text="View Bookings", command=lambda: self.app.show_frame(self.app.view_frame)).pack(pady=10) # This button takes me to view page
        tk.Button(self, text="Cancel Booking", command=lambda: self.app.show_frame(self.app.cancel_frame)).pack(pady=10) # This button takes me to cancel page
        tk.Button(self, text="Logout", command=lambda: self.app.show_frame(self.app.login_frame)).pack(pady=10) # This button takes me back to login page

# Booking frame class
class BookingFrame(BaseFrame):
    def __init__(self, parent, app, system):
        super().__init__(parent)
        self.app = app # Reference to FlightApp
        self.system = system # Reference to ReservationSystem

        tk.Label(self, text="Book a Flight", font=("Arial", 16)).pack(pady=10)
        tk.Label(self, text="Your Name:").pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        tk.Label(self, text="Select Flight:").pack()
        self.flight_var = tk.StringVar()
        self.flight_var.set(self.system.flights[0].code if self.system.flights else "") # Set default

        self.selected_flight_label = tk.Label(self, text="", fg="gray")
        self.selected_flight_label.pack()


        self.flight_var.trace("w", self.update_flight_info)
        self.flight_options = [flight.code for flight in self.system.flights]
        self.flight_menu = tk.OptionMenu(self, self.flight_var, *self.flight_options)
        self.flight_menu.pack()

        tk.Button(self, text="Book", command=self.handle_booking).pack(pady=5)
        tk.Button(self, text="Back", command=lambda: self.app.show_frame(self.app.main_frame)).pack()

        self.update_flight_info() # Initialize flight info

    def update_flight_info(self, *args):
        code = self.flight_var.get()
        flight = self.system.get_flight(code)
        if flight:
            self.selected_flight_label.config(text=f"{flight.destination} at {flight.date_time}")
        else:
            self.selected_flight_label.config(text="")

    def handle_booking(self):
        name = self.name_entry.get().strip()
        code = self.flight_var.get()
        flight = self.system.book_flight(name, code)
        if flight:
            messagebox.showinfo("Success", f"{name} booked on {flight}")
            self.name_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Invalid name or flight code.")

    def refresh_flight_menu(self):
        # Update the flight dropdown menu
        self.flight_menu["menu"].delete(0, "end")
        self.flight_options = [flight.code for flight in self.system.flights]
        for code in self.flight_options:
            self.flight_menu["menu"].add_command(label=code, command=tk._setit(self.flight_var, code))
        self.flight_var.set(self.system.flights[0].code if self.system.flights else "")


# View booking frame class
class ViewFrame(BaseFrame):
    def __init__(self, parent, app, system):
        super().__init__(parent)
        self.app = app
        self.system = system

        tk.Label(self, text="View Booking", font=("Arial", 16)).pack(pady=10)
        tk.Label(self, text="Your Name:").pack()
        self.view_name_entry = tk.Entry(self) # Text box for name
        self.view_name_entry.pack()

        tk.Button(self, text="View", command=self.handle_view).pack(pady=5)
        tk.Button(self, text="Back", command=lambda: self.app.show_frame(self.app.main_frame)).pack()

    def handle_view(self):
        name = self.view_name_entry.get()
        flight = self.system.view_booking(name)
        if flight:
            messagebox.showinfo("Booking Found", f"{name} is booked on {flight}")
        else:
            messagebox.showerror("Not Found", "No booking found.")

# Cancel booking frame class
class CancelFrame(BaseFrame):
    def __init__(self, parent, app, system):
        super().__init__(parent)
        self.app = app
        self.system = system

        tk.Label(self, text="Cancel Booking", font=("Arial", 16)).pack(pady=10)
        tk.Label(self, text="Your Name:").pack()
        self.cancel_name_entry = tk.Entry(self) # Text box for name
        self.cancel_name_entry.pack()

        tk.Button(self, text="Cancel Booking", command=self.handle_cancel).pack(pady=5)
        tk.Button(self, text="Back", command=lambda: self.app.show_frame(self.app.main_frame)).pack()

    def handle_cancel(self):
        name = self.cancel_name_entry.get()
        if self.system.cancel_booking(name):
            messagebox.showinfo("Cancelled", f"Booking for {name} has been cancelled.")
        else:
            messagebox.showerror("Error", "No booking found to cancel.")

# Admin frame class
class AdminFrame(BaseFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        tk.Label(self, text="Admin Dashboard", font=("Arial", 20)).pack(pady=20) # Title for Admin page
        tk.Label(self, text="Welcome, Admin", font=("Arial", 12)).pack(pady=10) # Welcome message
        tk.Button(self, text="Manage Flights", command=lambda: self.app.show_frame(self.app.manage_flights_frame)).pack(pady=10)
        tk.Button(self, text="Logout", command=lambda: self.app.show_frame(self.app.login_frame)).pack(pady=10)

# Manage flights frame class
class ManageFlightsFrame(BaseFrame):
    def __init__(self, parent, app, system):
        super().__init__(parent)
        self.app = app
        self.system = system

        tk.Label(self, text="All Available Flights", font=("Arial", 16)).pack(pady=10)
        self.flights_text = tk.Text(self, width=40, height=10)
        self.flights_text.pack(pady=5)
        self.display_flights() # Load flights initially

        tk.Button(self, text="Add Flight", command=lambda: self.app.show_frame(self.app.add_flight_frame)).pack(pady=10)
        tk.Label(self, text="Flight Code to Delete:").pack()
        self.delete_code_entry = tk.Entry(self)
        self.delete_code_entry.pack()

        tk.Button(self, text="Delete Flight", command=self.handle_delete_flight).pack(pady=5)
        tk.Button(self, text="Back", command=lambda: self.app.show_frame(self.app.admin_frame)).pack(pady=10)

    def display_flights(self):
        self.flights_text.delete("1.0", tk.END) # Clear previous text
        for flight in self.system.flights: # Loop through all flight objects
            self.flights_text.insert(tk.END, f"{flight}\n") # Add each to the text box

    def handle_delete_flight(self):
        code = self.delete_code_entry.get().strip()
        if self.system.delete_flight(code):
            messagebox.showinfo("Success", f"Flight {code} deleted.")
            self.display_flights() # Refresh the flight list
            self.delete_code_entry.delete(0, tk.END)
            self.app.booking_frame.refresh_flight_menu() # Update booking dropdown
        else:
            messagebox.showerror("Error", "Flight not found or has bookings.")

# Add flight frame class
class AddFlightFrame(BaseFrame):
    def __init__(self, parent, app, system):
        super().__init__(parent)
        self.app = app
        self.system = system

        tk.Label(self, text="Add New Flight", font=("Arial", 16)).pack(pady=10)
        tk.Label(self, text="Flight Code:").pack()
        self.new_code_entry = tk.Entry(self)
        self.new_code_entry.pack()

        tk.Label(self, text="Destination:").pack()
        self.new_destination_entry = tk.Entry(self)
        self.new_destination_entry.pack()

        tk.Label(self, text="Date & Time (YYYY-MM-DD HH:MM):").pack()
        self.new_datetime_entry = tk.Entry(self)
        self.new_datetime_entry.pack()

        tk.Button(self, text="Submit", command=self.add_new_flight).pack(pady=10)
        tk.Button(self, text="Back", command=lambda: self.app.show_frame(self.app.manage_flights_frame)).pack()

    def add_new_flight(self):
        # Get user input from the entry boxes
        code = self.new_code_entry.get()
        destination = self.new_destination_entry.get()
        date_time = self.new_datetime_entry.get()

        # Basic validation: make sure none are empty
        if not code or not destination or not date_time:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Create a new Flight object with entered info
        new_flight = Flight(code, destination, date_time)
        self.system.flights.append(new_flight)
        self.system.save_flights() # Save to file

        messagebox.showinfo("Success", f"Flight {code} added successfully!")
        self.new_code_entry.delete(0, tk.END)
        self.new_destination_entry.delete(0, tk.END)
        self.new_datetime_entry.delete(0, tk.END)

        self.app.manage_flights_frame.display_flights() # Refresh flight list
        self.app.booking_frame.refresh_flight_menu() # Update booking dropdown
        self.app.show_frame(self.app.manage_flights_frame) # Go back

# Main application class
class FlightApp:
    def __init__(self):
        self.system = ReservationSystem() # Create system object
        self.window = tk.Tk() # Create main window
        self.window.title("Shabo Airline") # Window title
        self.window.geometry("400x500") # Size of the window

        # Instantiate all frames
        self.login_frame = LoginFrame(self.window, self)
        self.main_frame = MainFrame(self.window, self)
        self.booking_frame = BookingFrame(self.window, self, self.system)
        self.view_frame = ViewFrame(self.window, self, self.system)
        self.cancel_frame = CancelFrame(self.window, self, self.system)
        self.admin_frame = AdminFrame(self.window, self)
        self.manage_flights_frame = ManageFlightsFrame(self.window, self, self.system)
        self.add_flight_frame = AddFlightFrame(self.window, self, self.system)

        self.show_frame(self.login_frame) # Show login page first

    def show_frame(self, frame):
        frame.tkraise() # Brings the chosen frame to the front

    def run(self):
        self.window.mainloop() # Run the app

# Start the application
if __name__ == "__main__":
    app = FlightApp()
    app.run()