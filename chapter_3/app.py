from flask       import Flask, render_template, request, session, redirect
from flask.views import MethodView
from random      import randrange

app = Flask(__name__)
app.secret_key = b"random string..."

member_data  = {}
message_data = []

@app.route("/", methods=["GET"])
def index():
    global message_data
    if "login" in session and session["login"]:
        msg = f"Login ID: {session['id']}"
        return render_template(
                "message.html", 
                title="Messages",
                message=msg,
                data=message_data,
                )
    else:
        return redirect("/login")

@app.route("/", methods=["POST"])
def form():
    global message_data
    msg = request.form.get("comment")
    message_data.append((session["id"], msg))
    message_data = message_data[-25:]
    return redirect("/")

@app.route("/login", methods=["GET"])
def login():
    return render_template(
            "login.html", 
            title="Login",
            err=False, 
            message="IDとパスワードを入力: ", 
            id="",
            )

@app.route("/login", methods=["POST"])
def login_post():
    global member_data
    id   = request.form.get("id")
    pswd = request.form.get("pass")

    if id in member_data:
        session["login"] = (pswd == member_data[id])
    else:
        member_data[id]  = pswd
        session["login"] = True

    session["id"] = id
    
    if session["login"]:
        return redirect("/")
    else:
        return render_template(
                "login.html", 
                title="Login",
                err=True, 
                message="パスワードが違います", 
                id=id,
                )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
