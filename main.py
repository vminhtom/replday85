import os
from flask import Flask, redirect, request, session
from replit import db

app = Flask(__name__)
app.secret_key = os.environ['sessionKey']


@app.route("/signup", methods=["POST"])
def createUser():
  # if session.get("loggedIn"):
  #   return redirect("/welcome")
  keys = db.keys()
  print(keys)
  form = request.form
  if form["username"] not in keys:
    print(form["username"])
    db[form["username"]] = {"username": form["username"], "password": form["password"], "name": form["name"]}
    return redirect("/login")
  else:
    return redirect("/signup")


@app.route("/login", methods=["POST"])
def doLogin():
  print("Execute function doLogin")
  # if session.get("loggedIn"):
  #   return redirect("/welcome")
  allkeys = db.keys()
  print(allkeys)
  print("===============")
  form = request.form
  username = form.get("username")
  password = form.get("password")

  # Check if the username exists in the database
  if username in db:
    # Check if the password matches
    print("checking password...")
    if password == db[username]["password"]:
      session["sessionKey"] = username
      return redirect("/welcome")
    else:
      print("Incorrect password")
      return redirect("/login")
  else:
    print("Username not found")
    return redirect("/login")


@app.route("/welcome")
def welcome():
  page = ""
  if session.get("sessionKey"):
    print("Execute function welcome")
    loggedInName = ""
    try:
      loggedInName = db[session["sessionKey"]]["name"]
    except Exception as err:
      print(err)

    page = f"""<h1>Hi {loggedInName}</h1>
  <button type="button" onClick="location.href='/logout'">Logout</button>
  """
  return page


@app.route("/logout")
def logout():
  session.clear()
  return redirect("/")


@app.route("/login")
def login():
  # if session.get("loggedIn"):
  #   return redirect("/welcome")
  page = ""
  with open("login.html", "r") as f:
    page = f.read()
  f.close()
  return page


@app.route("/signup")
def signup():
  # if session.get("loggedIn"):
  #   return redirect("/welcome")
  with open("signup.html", "r") as f:
    page = f.read()
  f.close()
  return page


@app.route('/')
def index():
  # if session.get("loggedIn"):
  #   return redirect("/welcome")
  page = """<p><a href="/signup">Sign up</a></p>
    <p><a href="/login">Log in</a></p>"""
  return page

@app.route("/reset")
def reset():
  session.clear()
  return redirect("/")

allkeys = db.keys()
print(allkeys)
# for eachKey in allkeys:
#   del db[eachKey]
app.run(host='0.0.0.0', port=81)
