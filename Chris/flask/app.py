from flask import Flask, render_template
import datetime

app = Flask(__name__)

@app.route("/")
def bonjour():
    return render_template("index.html")

@app.route("/heure")
def heure():
    date_heure = datetime.datetime.now()
    h = date_heure.hour
    m = date_heure.minute
    s = date_heure.second
    print(h, m, s)

    return render_template("heure.html", heure=h, minute=m, seconde=s)

    return f"heure H={h} M={m} S={s}"

if __name__ == '__name__':
    app.run(host="0.0.0.0", port=8000, debug=True)
