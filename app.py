from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "message": "Twitter API is running"
    })

@app.route("/api/twitter/<username>")
def twitter(username):
    username = username.lstrip("@")

    url = f"https://api.fxtwitter.com/user/{username}/tweets"

    try:
        response = requests.get(url, timeout=15)

        if response.status_code != 200:
            return jsonify({
                "status": "error",
                "message": "Could not get tweets"
            }), response.status_code

        data = response.json()

        return jsonify(data)

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
