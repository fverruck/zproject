#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 23:03:04 2019

@author: fabioverruck
"""

import os
import calendar
import sqlite3
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd



# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
    
@app.route("/")
def home():
    return render_template("layout.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    # RUN WHEN USER SUBMIT REGISTRATION
    if request.method == "POST":

        # hash password to protect user
        hash = generate_password_hash(request.form.get("password"))
        #open z.db database to start manipulation
        users = sqlite3.connect('/Users/fabioverruck/Documents/MACHINE_LEARNING/Zproject/z.db')  
        # create a cursor to manipulate data in z.db
        cursor = users.cursor()
        # store username and password in data variable
        data = [(request.form.get("username"), hash)]
        #insert data (username, password) into z.db
        new_user = cursor.executemany("INSERT INTO users (username, password) VALUES (?, ?)", data)
        
        users.commit()

        #confirm username and password were provided
        if not request.form.get("username") or not request.form.get("password") or not request.form.get("confirmation"):
            return apology(400)

        # confirm that user typed password correctly and return apology if no
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        #confirm that user did not type a blank space into username
        elif request.form.get("username").isspace():
            return apology("blank spaces are not allowed", 400)
        
        #verify if the user does not already exist
        elif not new_user:
            return redirect("/register", 400)
        
        #Registration logic
        else:

                    
            # allow new registrant to continue logged in after registration
            session["user_id"] = data[0][0]

            # show registered message after registration
            flash("Registered!")

            # redirect user to initial page after login
            return redirect("/")   


    # DEFAULT PAGE
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        #open z.db database to start manipulation
        users = sqlite3.connect('/Users/fabioverruck/Documents/MACHINE_LEARNING/Zproject/z.db')  
        # create a cursor to manipulate data in z.db
        cursor = users.cursor()
        # Query database for username
        user = request.form.get('username')
        cursor.execute("SELECT * FROM users WHERE username = ?", (user,))
        rows = cursor.fetchone()

        # Ensure username exists and password is correct
        if not check_password_hash(rows[1], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/check", methods=["GET"])
def check(username=""):
    #open z.db database to start manipulation
    users = sqlite3.connect('/Users/fabioverruck/Documents/MACHINE_LEARNING/Zproject/z.db')  
    # create a cursor to manipulate data in z.db
    cursor = users.cursor()
    username = request.args.get("username", username)
    look_up = cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
    if len(look_up) == 1:
        return jsonify(False)
    else:
        return jsonify(True)

@app.route("/schedule", methods=["GET", "POST"])
@login_required
def schedule():
    return render_template("schedule.html")


@app.route("/cadastro", methods=["GET", "POST"])
@login_required
def cadastro():
    negocio = request.form.get("negocio")
    ramo = request.form.get("ramo")
    return render_template("cadastro.html")


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
    