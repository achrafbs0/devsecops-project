#!/usr/bin/env python3
"""
Application Flask vulnérable pour démonstration DevSecOps
"""
import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)

# ➤ Secret key depuis variable d'environnement
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default_dev_secret_key")

app.config['DEBUG'] = True

# ➤ Variables sensibles via env vars
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


@app.route("/")
def home():
    return "<h1>Bienvenue sur mon app DevSecOps !</h1>"


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]

        conn = sqlite3.connect('vulnerable_app.db')
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                           (username, password, email))
            conn.commit()
            flash("✅ Inscription réussie, vous pouvez vous connecter.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("⚠️ Nom d’utilisateur déjà pris.", "danger")
        finally:
            conn.close()

    return '''
        <h2>Inscription</h2>
        <form method="post">
            <input type="text" name="username" placeholder="Nom d'utilisateur" required><br>
            <input type="email" name="email" placeholder="Email" required><br>
            <input type="password" name="password" placeholder="Mot de passe" required><br>
            <button type="submit">S'inscrire</button>
        </form>
    '''


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect('vulnerable_app.db')
        cursor = conn.cursor()

        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        print("DEBUG SQL QUERY -->", query)
        cursor.execute(query)

        user = cursor.fetchone()
        conn.close()

        if user:
            session["user"] = username
            flash("✅ Connecté avec succès.", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("❌ Identifiants invalides.", "danger")

    return '''
        <h2>Connexion</h2>
        <form method="post">
            <input type="text" name="username" placeholder="Nom d'utilisateur" required><br>
            <input type="password" name="password" placeholder="Mot de passe" required><br>
            <button type="submit">Se connecter</button>
        </form>
    '''


@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return f"<h2>Bienvenue, {session['user']} ! Ceci est ton tableau de bord.</h2>"
    else:
        flash("⚠️ Vous devez être connecté pour accéder au tableau de bord.", "warning")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("✅ Déconnecté.", "success")
    return redirect(url_for("home"))


if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
