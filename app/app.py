#!/usr/bin/env python3
"""
Application Flask vulnérable pour démonstration DevSecOps
"""
import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
import subprocess

app = Flask(__name__)

# ➤ Correction : remplace le secret key en dur par variable d'environnement
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default_dev_secret_key")

app.config['DEBUG'] = True

# ➤ Correction : remplace clés/API hardcodées par variables d'environnement
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID", "dummy_access_key")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "dummy_db_password")

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

    conn.commit()
    conn.close()
