from flask import Flask, render_template, redirect, request, url_for, flash, session
import sqlite3
import os
app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Initialize the database
def init_db():
    with sqlite3.connect('wastewater.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            phone TEXT NOT NULL,
            username TEXT UNIQUE,
            password TEXT NOT NULL
        )''')
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

init_db()

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        phone = request.form['phone']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))

        
        try:
            conn = sqlite3.connect('wastewater.db')
            cur = conn.cursor()
            cur.execute('INSERT INTO users (email, phone, username, password) VALUES (?, ?, ?, ?)',
                        (email, phone, username, password))
            conn.commit()
            conn.close()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists!', 'danger')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        
        conn = sqlite3.connect('wastewater.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
        user = cur.fetchone()
        conn.close()

        if user:
            session['user'] = user[0]  
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')


@app.route('/add_results', methods=['GET', 'POST'])
def add_results():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        ph_untreated = request.form['ph_untreated']
        ph_treated = request.form['ph_treated']
        chloride_untreated = request.form['chloride_untreated']
        chloride_treated = request.form['chloride_treated']
        solid_untreated = request.form['solid_untreated']
        solid_treated = request.form['solid_treated']
        nitrogen_untreated = request.form['nitrogen_untreated']
        nitrogen_treated = request.form['nitrogen_treated']
        bod_untreated = request.form['bod_untreated']
        bod_treated = request.form['bod_treated']
        oxygen_untreated = request.form['oxygen_untreated']
        oxygen_treated = request.form['oxygen_treated']

        with sqlite3.connect('wastewater.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO results 
                (ph_untreated, ph_treated, chloride_untreated, chloride_treated, 
                solid_untreated, solid_treated, nitrogen_untreated, nitrogen_treated, 
                bod_untreated, bod_treated, oxygen_untreated, oxygen_treated) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (ph_untreated, ph_treated, chloride_untreated, chloride_treated, 
                solid_untreated, solid_treated, nitrogen_untreated, nitrogen_treated, 
                bod_untreated, bod_treated, oxygen_untreated, oxygen_treated))
            conn.commit()

        return redirect(url_for('show_results'))

        # Log inserted data
        print(f"Inserted data: {ph_untreated}, {ph_treated}, {chloride_untreated}, {chloride_treated}, "
              f"{solid_untreated}, {solid_treated}, {nitrogen_untreated}, {nitrogen_treated}, "
              f"{bod_untreated}, {bod_treated}, {oxygen_untreated}, {oxygen_treated}")

        return redirect(url_for('show_results'))


    return render_template('add_results.html')


@app.route('/show_results')
def show_results():
    if 'user' not in session:
        return redirect(url_for('login'))
    with sqlite3.connect('wastewater.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM results")
        results = cursor.fetchall()
    return render_template('show_results.html', results=results)


@app.route('/edit_result/<int:result_id>', methods=['GET', 'POST'])
def edit_result(result_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('wastewater.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        ph_untreated = request.form['ph_untreated']
        ph_treated = request.form['ph_treated']
        chloride_untreated = request.form['chloride_untreated']
        chloride_treated = request.form['chloride_treated']
        solid_untreated = request.form['solid_untreated']
        solid_treated = request.form['solid_treated']
        nitrogen_untreated = request.form['nitrogen_untreated']
        nitrogen_treated = request.form['nitrogen_treated']
        bod_untreated = request.form['bod_untreated']
        bod_treated = request.form['bod_treated']
        oxygen_untreated = request.form['oxygen_untreated']
        oxygen_treated = request.form['oxygen_treated']

        cursor.execute('''
        UPDATE results SET 
            ph_untreated = ?, ph_treated = ?, chloride_untreated = ?, chloride_treated = ?, 
            solid_untreated = ?, solid_treated = ?, nitrogen_untreated = ?, nitrogen_treated = ?, 
            bod_untreated = ?, bod_treated = ?, oxygen_untreated = ?, oxygen_treated = ?
        WHERE id = ?''',
        (ph_untreated, ph_treated, chloride_untreated, chloride_treated, 
         solid_untreated, solid_treated, nitrogen_untreated, nitrogen_treated, 
         bod_untreated, bod_treated, oxygen_untreated, oxygen_treated, result_id))
        conn.commit()
        conn.close()

        flash('Result updated successfully!', 'success')
        return redirect(url_for('show_results'))
    
    cursor.execute('SELECT * FROM results WHERE id = ?', (result_id,))
    result = cursor.fetchone()
    conn.close()
    
    return render_template('edit_result.html', result=result)




@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

