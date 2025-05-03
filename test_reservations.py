from ArlineCode import ReservationSystem

# Set up the system globally for all tests
def setup_function():
    global rs
    rs = ReservationSystem()

# Test booking a valid flight
def test_book_valid_flight():
    result = rs.book_flight("Amir", "LA123")
    assert result is not None
    assert result.code == "LA123"  # Access flight code from Flight object
    assert rs.bookings["Amir"] == "LA123"  # Confirm booking exists in the system

# Test booking an invalid flight code
def test_book_invalid_flight_code():
    result = rs.book_flight("Jeff", "INVALID")
    assert result is None  # Invalid flight should return None

# Test canceling an existing booking
def test_cancel_existing_booking():
    rs.book_flight("Amir", "LA123")  # First, book a valid flight
    result = rs.cancel_booking("Amir")  # Now cancel it
    assert result is True  # Cancel should succeed

# Test canceling a booking that doesn't exist
def test_cancel_nonexistent_booking():
    result = rs.cancel_booking("Charlie")  # Charlie never booked
    assert result is False  # Cancel should fail