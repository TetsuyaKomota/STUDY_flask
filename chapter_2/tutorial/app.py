from flask       import Flask, render_template, request
from flask.views import MethodView
from random      import randrange

app = Flask(__name__)

class HelloAPI(MethodView):
    send = ""

    def get(self):
        return render_template(
                "next.html", 
                title="Next page",
                message="何か書いてください", 
                send=HelloAPI.send, 
                )

    def post(self):
        HelloAPI.send = request.form.get("send")
        return render_template(
                "next.html", 
                title="Next page",
                message=f"You send: {HelloAPI.send}", 
                send=HelloAPI.send, 
                )

@app.template_filter("sum")
def sum_filter(data):
    return sum(data)

app.jinja_env.filters["sum"] = sum_filter
app.add_url_rule("/hello", view_func=HelloAPI.as_view("hello"))

@app.context_processor
def sample_processor():
    def total(n):
        return sum(range(1, n+1))
    return {"total": total}

@app.route("/")
def index():
    data = [randrange(0, 100) for _ in range(randrange(5, 10))]
    return render_template(
            "index.html", 
            title="Index with Jinja", 
            message="これはJinjaテンプレートの利用例です", 
            data=data
            )

@app.route("/<id>/<password>")
def index2(id, password):
    # msg  = f"id: {id}, password:{password}"
    msg  = "<a href='/'>go to top page</a>"
    flg  = (id in ["tkomota"])
    data = ["Windows", "macOS", "Linux", "ChromeOS"]
    return render_template(
            "index.html", 
            title="Index with Jinja", 
            message=msg, 
            flg=flg, 
            data=data,
            unknown="known"
            )

@app.route("/next", methods=["GET"])
def next():
    return render_template(
            "next.html", 
            title="Next page", 
            message="※ これは 別ページのサンプルです", 
            data=["one", "two", "three"], 
            )



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
