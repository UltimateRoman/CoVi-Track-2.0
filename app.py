from cs50 import SQL
import requests, json
from flask import Flask, flash, render_template, request, redirect, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import config

from helpers import login_required

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///maindb.db")

@app.route("/")
def index():
    response0 = requests.get(config.url0)
    data0 = json.loads(response0.text)
    return render_template("index.html", data0=data0)

@app.route("/country", methods = ["GET", "POST"])
def country():
    if request.method == "GET":
        return render_template("country.html")
    else:
        cname = request.form.get("cname")
        if not cname:
            flash("Missing country name")
            return redirect("/country")
        response1 = requests.get(config.url1+cname)
        data1 = json.loads(response1.text)
        if 'message' in data1:
            data1 = None
        if data1 == None:
            flash("Country could not be found")
            return redirect("/country")
        return render_template("country.html", data1=data1)

@app.route("/instates", methods = ["GET", "POST"])
def instates():
    if request.method == "GET":
        return render_template("instates.html")
    else:
        sname = request.form.get("sname")
        if not sname:
            flash("Missing state/UT name")
            return redirect("/instates")
        response3 = requests.get(config.url3)
        dt = json.loads(response3.text)
        dt1 = dt['data']['regional']
        f = 0
        for st in dt1:
            if st['loc'] == sname:
                data3 = st
                f = 1
        if not f:
            data3 = None
        if data3 == None:
            flash("State/UT could not be found")
            return redirect("/instates")
        return render_template("instates.html", data3=data3)

@app.route("/usstates", methods = ["GET", "POST"])
def usstates():
    if request.method == "GET":
        return render_template("usstates.html")
    else:
        sname = request.form.get("sname")
        if not sname:
            flash("Missing state name")
            return redirect("/usstates")
        response2 = requests.get(config.url2+sname)
        data2 = json.loads(response2.text)
        if 'message' in data2:
            data2 = None
        if data2 == None:
            flash("State could not be found")
            return redirect("/usstates")
        return render_template("usstates.html", data2=data2)


@app.route("/login", methods = ["GET", "POST"])
def login():
    session.clear()
    if request.method == "GET":
        return render_template("login.html")
    else:
        if not request.form.get("username"):
            flash("Must provide username")
            return redirect("/login")
        elif not request.form.get("password"):
            flash("Must provide password")
            return redirect("/login")
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Invalid username and/or password!")
            return redirect("/login")
        session["user_id"] = rows[0]["id"]
        return redirect("/home")

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if not request.form.get("username"):
        flash("Username field is blank!")
        return redirect("/register")

    elif not request.form.get("password"):
        flash("Password field is blank!")
        return redirect("/register")

    elif request.form.get("password") != request.form.get("confirmation"):
        flash("Passwords do not match!")
        return redirect("/register")
    else:
        hashpwd = generate_password_hash(request.form.get("password"))
        musrs = db.execute("SELECT * FROM users WHERE username=:username",
                             username=request.form.get("username"))
        if len(musrs) != 0:
            flash("Username not available!")
            return redirect("/register")
        resp = db.execute("INSERT INTO users(username, hash) VALUES(:username, :hash)",
                              username=request.form.get("username"),
                              hash=hashpwd)
        session["user_id"] = resp
        return redirect("/home")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/home")
@login_required
def home():
    riskps = db.execute("SELECT rp FROM users WHERE id=:cid", cid=session["user_id"])[0]["rp"]
    tdata = db.execute("SELECT rpchange FROM records WHERE user=:cid AND actdate=CURRENT_DATE", cid=session["user_id"])
    if tdata:
        return render_template("home.html", riskps=riskps, tpoints=tdata[0]["rpchange"])
    else:
        return render_template("home.html", riskps=riskps)

@app.route("/history")
@login_required
def history():
    records = db.execute("SELECT * FROM records WHERE user=:cid", cid=session["user_id"])
    return render_template("history.html", records=records)

@app.route("/dailysa", methods=['GET', 'POST'])
@login_required
def dailysa():
    if request.method == "GET":
        cdate = db.execute("SELECT CURRENT_DATE")[0]['CURRENT_DATE']
        ldate = db.execute("SELECT actdate FROM records GROUP BY user HAVING user=:cid ORDER BY actdate DESC",
                            cid=session["user_id"])
        if ldate:
            if cdate == ldate[0]['actdate']:
                flash("Your next round of self-analysis will be available tomorrow")
                return redirect("/home")
            else:
                return render_template("dailysa.html")
        else:
            return render_template("dailysa.html")
    else:
        val = request.form.getlist("hello")
        rp = 0
        for sno in val:
            if sno == '1':
                rp += 8
            elif sno == '2':
                rp += 10
            elif sno == '3':
                rp += 4
            elif sno == '4':
                rp += 6
            elif sno == '5':
                rp += 0
            elif sno == '6':
                rp += 6
            elif sno == '7':
                rp += 7
            elif sno == '8':
                rp += 7
            elif sno == '9':
                rp += 5
            elif sno == '10':
                rp += 6
        ogrp = db.execute("SELECT rp FROM users WHERE id = :cid", cid=session["user_id"])[0]["rp"]
        if rp <= ogrp:
            if ogrp <= 6:
                rp = ogrp/2
            else:
                rp = rp + ogrp/5
        else:
            if rp <= 6:
                rp += ogrp/8
            else:
                rp += ogrp/4
        rpchange = rp - ogrp
        db.execute("UPDATE users SET rp = :rp WHERE id = :cid",
                    rp=rp,
                    cid=session["user_id"])
        db.execute("INSERT INTO records(rpchange, user, prevrp, newrp, actdate) VALUES(:rpchange, :cid, :ogrp, :newrp, current_date)",
                    rpchange=rpchange, cid=session["user_id"], ogrp=ogrp, newrp=rp)
        return redirect("/home")