import sqlite3

# Function to initialize the database
def init_db():
    with sqlite3.connect('wastewater.db') as conn:
        cursor = conn.cursor()

        # Create the users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            phone TEXT NOT NULL,
            username TEXT UNIQUE,
            password TEXT NOT NULL
        )''')

        # Create the results table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ph_untreated REAL,
            ph_treated REAL,
            chloride_untreated REAL,
            chloride_treated REAL,
            solid_untreated REAL,
            solid_treated REAL,
            nitrogen_untreated REAL,
            nitrogen_treated REAL,
            bod_untreated REAL,
            bod_treated REAL,
            oxygen_untreated REAL,
            oxygen_treated REAL
        )''')

    print("Database and tables created successfully.")

# Run the database initialization
if __name__ == '__main__':
    init_db()
