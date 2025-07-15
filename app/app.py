#!/usr/bin/env python3
"""
Application Flask vulnérable pour démonstration DevSecOps
"""
import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
import subprocess

app = Flask(__name__)
app.secret_key = "super_secret_key_123"  # Secret hardcodé
app.config['DEBUG'] = True

# Clés API hardcodées (vulnérabilité intentionnelle)
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
DATABASE_PASSWORD = "admin123"

def init_db():
    """Initialise la base de données"""
    conn = sqlite3.connect('vulnerable_app.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    
    try:
        cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                      ("admin", "admin", "admin@example.com"))
        cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                      ("user", "password123", "user@example.com"))
    except sqlite3.IntegrityError:
        pass
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Authentification vulnérable à l'injection SQL"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('vulnerable_app.db')
        cursor = conn.cursor()
        
        # VULNÉRABILITÉ : Injection SQL
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['username'] = user[1]
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/search')
def search():
    """Recherche vulnérable"""
    query = request.args.get('q', '')
    
    if query:
        conn = sqlite3.connect('vulnerable_app.db')
        cursor = conn.cursor()
        
        # Vulnérabilité SQL Injection
        sql = f"SELECT * FROM users WHERE username LIKE '%{query}%'"
        cursor.execute(sql)
        results = cursor.fetchall()
        conn.close()
        
        return render_template('search.html', results=results, query=query)
    
    return render_template('search.html', results=[], query='')

@app.route('/execute')
def execute_command():
    """Exécution de commandes vulnérable"""
    command = request.args.get('cmd', 'ls')
    
    # Vulnérabilité : Injection de commandes
    try:
        result = subprocess.check_output(command, shell=True, text=True)
        return f"<pre>{result}</pre>"
    except subprocess.CalledProcessError as e:
        return f"Erreur: {e}"

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
