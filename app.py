from flask import Flask, render_template, request, jsonify
import sqlite3
import random

app = Flask(__name__)

# Create database and table
def init_db():
    conn = sqlite3.connect('bus_reservation.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        bus_number TEXT,
        pickup TEXT,
        destination TEXT,
        travel_date TEXT,
        seat_number INTEGER
    )''')
    conn.commit()
    conn.close()

init_db()

# Route for homepage
@app.route('/')
def home():
    return render_template('index.html')

# Route for booking page
@app.route('/book')
def book_page():
    return render_template('book.html')

# Route to handle booking
@app.route('/book_ticket', methods=['POST'])
def book_ticket():
    data = request.json
    pickup = data['pickup']
    destination = data['destination']
    travel_date = data['travel_date']
    seat_number = data['seat_number']

    user_id = f"{random.randint(1, 999)}"  # Generate unique user_id
    bus_number = f"BUS{random.randint(100, 999)}"  # Generate bus_number

    conn = sqlite3.connect('bus_reservation.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tickets (user_id, bus_number, pickup, destination, travel_date, seat_number) VALUES (?, ?, ?, ?, ?, ?)",
                   (user_id, bus_number, pickup, destination, travel_date, seat_number))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Ticket booked successfully! User ID: {user_id}, Bus Number: {bus_number}"})


if __name__ == '__main__':
    app.run(debug=True)
