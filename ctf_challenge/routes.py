import json
from flask import Flask, redirect, render_template, flash, url_for, session, abort
from forms import LoginForm
import pyodbc


app = Flask(__name__)


with open("config.json") as f:
    json_config = json.load(f)
    app.config["SECRET_KEY"] = json_config["SECRET_KEY"]
    FLAG = json_config["FLAG"]


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        try:
            connection = pyodbc.connect(f"DRIVER={{ODBC Driver 18 for SQL Server}};TrustServerCertificate=yes;UID={username};PWD={password};SERVER=mssql;", timeout=7)
            connection.close()
            session["username"] = "admin"
            session.modified = True
            flash("Logged in!", "success")
            return redirect(url_for("flag"))
            
        except Exception as e:
            flash(e, "danger")
            return render_template("login.html", form=form)

    return render_template("login.html", form=form)


@app.route("/flag")
def flag():
    if session.get("username") == "admin":
        return render_template("flag.html", FLAG=FLAG)
    else:
        return abort(401)
