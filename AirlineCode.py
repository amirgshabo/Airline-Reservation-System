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
  
   def get_all_bookings_report(self):
       report = []
       for name, code in self.bookings.items():
           flight = self.get_flight(code)
           if flight:
               report.append(f"Passenger: {name}, Flight: {flight}")
       return "\n".join(report) if report else "No bookings found."
  
   def get_flights_summary_report(self):
       report = []
       for flight in self.flights:
           booking_count = sum(1 for name, code in self.bookings.items() if code == flight.code)
           report.append(f"{flight} - Bookings: {booking_count}")
       return "\n".join(report) if report else "No flights available."

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
               self.app.current_user = user_name # Store user name
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
               self.app.current_user = "Admin" # Store admin as user
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
       tk.Button(self, text="Logout", command=self.handle_logout).pack(pady=10) # This button takes me back to login page

   def handle_logout(self):
       self.app.current_user = "" # Clear current user
       self.app.show_frame(self.app.login_frame) # Go to login page

# Booking frame class
class BookingFrame(BaseFrame):
    def __init__(self, parent, app, system):
        super().__init__(parent)
        self.app = app  # Reference to FlightApp
        self.system = system  # Reference to ReservationSystem
        self.configure(bg="#f0f4f8")  # Light background for better look

        # Main container for better organization
        container = tk.Frame(self, bg="#f0f4f8", padx=20, pady=20)
        container.pack(expand=True, fill="both")

        # Title with styled font and color
        tk.Label(
            container, 
            text="Book a Flight", 
            font=("Arial", 18, "bold"), 
            bg="#f0f4f8", 
            fg="#2c3e50"
        ).pack(pady=(0, 15))

        # User info frame
        user_frame = tk.Frame(container, bg="#f0f4f8")
        user_frame.pack(fill="x", pady=5)
        self.user_var = tk.StringVar()
        self.user_var.set(f"Booking for: {self.app.current_user}")
        tk.Label(
            user_frame, 
            textvariable=self.user_var, 
            font=("Arial", 12), 
            bg="#f0f4f8", 
            fg="#34495e"
        ).pack()

        # Flight selection frame with border
        flight_frame = tk.LabelFrame(
            container, 
            text=" Available Flights ", 
            font=("Arial", 12), 
            bg="#ffffff", 
            fg="#2c3e50", 
            bd=2, 
            relief="groove"
        )
        flight_frame.pack(fill="both", pady=10, padx=10)

        # Listbox for flights
        self.flight_listbox = tk.Listbox(
            flight_frame, 
            height=4, 
            font=("Arial", 11), 
            selectmode=tk.SINGLE, 
            bg="#ffffff", 
            fg="#2c3e50", 
            selectbackground="#3498db", 
            selectforeground="#ffffff"
        )
        self.flight_listbox.pack(fill="x", padx=5, pady=5)

        # Flight details display (ensured initialization)
        self.selected_flight_label = tk.Label(
            flight_frame, 
            text="No flight selected", 
            font=("Arial", 11, "italic"), 
            bg="#ffffff", 
            fg="#7f8c8d"
        )
        self.selected_flight_label.pack(pady=5)

        # Bind listbox selection to update details
        self.flight_listbox.bind("<<ListboxSelect>>", self.update_flight_info)

        # Populate listbox after initialization
        self.update_flight_listbox()

        # Buttons frame for consistent alignment
        button_frame = tk.Frame(container, bg="#f0f4f8")
        button_frame.pack(fill="x", pady=15)

        # Styled book button
        tk.Button(
            button_frame, 
            text="Book Flight", 
            font=("Arial", 12, "bold"), 
            bg="#3498db", 
            fg="#ffffff", 
            width=15, 
            relief="flat", 
            activebackground="#2980b9", 
            command=self.handle_booking
        ).pack(side="left", padx=10)

        # Styled back button
        tk.Button(
            button_frame, 
            text="Back", 
            font=("Arial", 12), 
            bg="#ecf0f1", 
            fg="#2c3e50", 
            width=10, 
            relief="flat", 
            activebackground="#bdc3c7", 
            command=lambda: self.app.show_frame(self.app.main_frame)
        ).pack(side="right", padx=10)

    def update_flight_listbox(self):
        # Populate listbox with flights
        self.flight_listbox.delete(0, tk.END)
        if not self.system.flights:
            self.flight_listbox.insert(tk.END, "No flights available")
            self.selected_flight_label.config(text="No flights available")
            return
        for flight in self.system.flights:
            self.flight_listbox.insert(tk.END, f"{flight.code}: {flight.destination} at {flight.date_time}")
        self.flight_listbox.select_set(0)  # Select first flight by default
        self.update_flight_info()  # Update details for default selection

    def update_flight_info(self, event=None):
        # Update flight details based on listbox selection
        if not self.system.flights:
            self.selected_flight_label.config(text="No flights available")
            return
        try:
            index = self.flight_listbox.curselection()[0]
            flight = self.system.flights[index]
            self.selected_flight_label.config(text=f"Selected: {flight.destination} at {flight.date_time}")
        except IndexError:
            self.selected_flight_label.config(text="No flight selected")

    def handle_booking(self):
        name = self.app.current_user
        if not self.system.flights:
            messagebox.showerror("Error", "No flights available to book.")
            return
        try:
            index = self.flight_listbox.curselection()[0]
            flight = self.system.flights[index]
            code = flight.code
            # Confirmation dialog
            confirm = messagebox.askyesno(
                "Confirm Booking", 
                f"Book {name} on {flight}?"
            )
            if confirm:
                booked_flight = self.system.book_flight(name, code)
                if booked_flight:
                    messagebox.showinfo("Success", f"{name} booked on {booked_flight}")
                    self.app.reports_frame.refresh_report()  # Update reports
                else:
                    messagebox.showerror("Error", "Booking failed.")
        except IndexError:
            messagebox.showerror("Error", "Please select a flight.")

    def refresh_flight_menu(self):
        # Update flight listbox (renamed for consistency)
        self.update_flight_listbox()

    def update_user_label(self):
        self.user_var.set(f"Booking for: {self.app.current_user}")

# View booking frame class
class ViewFrame(BaseFrame):
   def __init__(self, parent, app, system):
       super().__init__(parent)
       self.app = app # Reference to FlightApp
       self.system = system # Reference to ReservationSystem

       tk.Label(self, text="View Booking", font=("Arial", 16)).pack(pady=10)
       self.user_var = tk.StringVar()
       self.user_var.set(f"Viewing for: {self.app.current_user}") # Initialize user label
       tk.Label(self, textvariable=self.user_var).pack() # Text box for name

       tk.Button(self, text="View", command=self.handle_view).pack(pady=5)
       tk.Button(self, text="Back", command=lambda: self.app.show_frame(self.app.main_frame)).pack()

   def handle_view(self):
       name = self.app.current_user # Use logged-in user’s name
       flight = self.system.view_booking(name)
       if flight:
           messagebox.showinfo("Booking Found", f"{name} is booked on {flight}")
       else:
           messagebox.showerror("Not Found", "No booking found.")

   def update_user_label(self):
       self.user_var.set(f"Viewing for: {self.app.current_user}") # Update the user label

# Cancel booking frame class
class CancelFrame(BaseFrame):
   def __init__(self, parent, app, system):
       super().__init__(parent)
       self.app = app # Reference to FlightApp
       self.system = system # Reference to ReservationSystem

       tk.Label(self, text="Cancel Booking", font=("Arial", 16)).pack(pady=10)
       self.user_var = tk.StringVar()
       self.user_var.set(f"Canceling for: {self.app.current_user}") # Initialize user label
       tk.Label(self, textvariable=self.user_var).pack() # Text box for name

       tk.Button(self, text="Cancel Booking", command=self.handle_cancel).pack(pady=5)
       tk.Button(self, text="Back", command=lambda: self.app.show_frame(self.app.main_frame)).pack()

   def handle_cancel(self):
       name = self.app.current_user # Use logged-in user’s name
       if self.system.cancel_booking(name):
           messagebox.showinfo("Cancelled", f"Booking for {name} has been cancelled.")
           self.app.reports_frame.refresh_report() # Refresh reports after cancellation
       else:
           messagebox.showerror("Error", "No booking found to cancel.")

   def update_user_label(self):
       self.user_var.set(f"Canceling for: {self.app.current_user}") # Update the user label

# Admin frame class
class AdminFrame(BaseFrame):
   def __init__(self, parent, app):
       super().__init__(parent)
       self.app = app # Reference to FlightApp

       tk.Label(self, text="Admin Dashboard", font=("Arial", 20)).pack(pady=20) # Title for Admin page
       tk.Label(self, text="Welcome, Admin", font=("Arial", 12)).pack(pady=10) # Welcome message
       tk.Button(self, text="Manage Flights", command=lambda: self.app.show_frame(self.app.manage_flights_frame)).pack(pady=10)
       tk.Button(self, text="View Reports", command=lambda: self.app.show_frame(self.app.reports_frame)).pack(pady=10)
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

# Reports frame class
class ReportsFrame(BaseFrame):
   def __init__(self, parent, app, system):
       super().__init__(parent)
       self.app = app # Reference to FlightApp
       self.system = system # Reference to ReservationSystem
       self.current_report = None # Track current report type

       tk.Label(self, text="Manager Reports", font=("Arial", 16)).pack(pady=10) # Title for reports page
       self.report_text = tk.Text(self, width=50, height=15) # Text box for report output
       self.report_text.pack(pady=5)

       tk.Button(self, text="All Bookings Report", command=self.show_all_bookings).pack(pady=5) # Button for bookings report
       tk.Button(self, text="Flights Summary Report", command=self.show_flights_summary).pack(pady=5) # Button for flights report
       tk.Button(self, text="Back", command=lambda: self.app.show_frame(self.app.admin_frame)).pack(pady=10) # Back to admin menu

   def show_all_bookings(self):
       self.current_report = "bookings" # Set current report type
       self.report_text.delete("1.0", tk.END) # Clear text box
       report = self.system.get_all_bookings_report() # Get bookings report
       self.report_text.insert(tk.END, report) # Display report

   def show_flights_summary(self):
       self.current_report = "flights" # Set current report type
       self.report_text.delete("1.0", tk.END) # Clear text box
       report = self.system.get_flights_summary_report() # Get flights report
       self.report_text.insert(tk.END, report) # Display report

   def refresh_report(self):
       # Refresh the current report if one is displayed
       if self.current_report == "bookings":
           self.show_all_bookings()
       elif self.current_report == "flights":
           self.show_flights_summary()

# Main application class
class FlightApp:
   def __init__(self):
       self.system = ReservationSystem() # Create system object
       self.current_user = "" # Initialize current user
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
       self.reports_frame = ReportsFrame(self.window, self, self.system)

       self.show_frame(self.login_frame) # Show login page first

   def show_frame(self, frame):
       frame.tkraise() # Brings the chosen frame to the front
       if hasattr(frame, 'update_user_label'):
           frame.update_user_label() # Refresh frame if needed

   def run(self):
       self.window.mainloop() # Run the app

# Start the application
if __name__ == "__main__":
   app = FlightApp()
   app.run()