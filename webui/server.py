from flask import Flask, jsonify, render_template, send_from_directory

HOST = "0.0.0.0"
HOST = "192.168.43.66"

tee = lambda f, a: (a, f(a))[0]

app = Flask(__name__)

@app.route("/static/<path:path>")
def static_dir(path):
  return send_from_directory("static", path)

@app.route("/")
def root():
  return render_template("index.html")

@app.route("/callback/<payload>")
def callback(payload):
  print(payload)
  try:
    return tee(lambda a:print(f"\n\n{a}\n"), jsonify(eval(payload)))
  except Exception as e:
    return jsonify({"error": str(e),
                    "raw": payload})

app.run(host=HOST, debug=True)
