from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection setup
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",  # or your DB host
        user="root",  # your DB username
        password="yourpassword",  # your DB password
        database="event_management"
    )

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Events page (list all events)
@app.route("/events")
def events():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()
    conn.close()
    return render_template("events.html", events=events)

# Create a new event (organizer functionality)
@app.route("/create-event", methods=["GET", "POST"])
def create_event():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        event_date = request.form["event_date"]
        venue_id = request.form["venue_id"]
        organizer_id = 1  # hardcoded for now (replace with logged-in user)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO events (title, description, event_date, venue_id, organizer_id) VALUES (%s, %s, %s, %s, %s)",
                       (title, description, event_date, venue_id, organizer_id))
        conn.commit()
        conn.close()

        return redirect(url_for("events"))

    return render_template("create-event.html")

# Register as attendee (user functionality)
@app.route("/register/<event_id>", methods=["GET", "POST"])
def register(event_id):
    if request.method == "POST":
        user_id = 1  # hardcoded for now (replace with logged-in user)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO attendees (user_id, event_id) VALUES (%s, %s)", (user_id, event_id))
        conn.commit()
        conn.close()

        return redirect(url_for("events"))

    return render_template("events.html")

# Admin panel to manage users, events, venues
@app.route("/admin")
def admin():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()

    cursor.execute("SELECT * FROM venues")
    venues = cursor.fetchall()

    conn.close()
    
    return render_template("admin.html", users=users, events=events, venues=venues)

if __name__ == "__main__":
    app.run(debug=True)
