from flask import Flask, jsonify

HOST = "0.0.0.0"
HOST = "192.168.43.66"

tee = lambda f, a: (a, f(a))[0]

app = Flask(__name__)

@app.route("/<payload>")
def callback(payload):
    print()
    try:
        return tee(lambda a:print(f"\n\n{a}\n"), jsonify(eval(payload)))
    except Exception as e:
        return jsonify({"error":str(e),
                        "raw":payload})

app.run(host=HOST)
