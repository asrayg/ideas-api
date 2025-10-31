from flask import Flask, request, jsonify
import json, random, time
from functools import wraps
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(get_remote_address, app=app, default_limits=["30 per hour"])

APPROVED = "approved.json"
PENDING = "pending.json"
ADMIN_TOKEN = "mysecretadminpass"  # change this for real use

# --- Helper functions ---
def load_json(filename):
    with open(filename, "r") as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

# --- Routes ---
@app.route("/ideas/random", methods=["GET"])
@limiter.limit("30 per hour")
def random_idea():
    ideas = load_json(APPROVED)
    return jsonify(random.choice(ideas))

@app.route("/ideas/submit", methods=["POST"])
def submit_idea():
    new_idea = request.get_json()
    required_fields = ["idea", "example", "author"]

    if not new_idea or any(field not in new_idea for field in required_fields):
        return jsonify({"error": f"Missing required fields: {', '.join(required_fields)}"}), 400

    pending = load_json(PENDING)
    idea_id = int(time.time())
    new_idea["id"] = idea_id
    pending.append(new_idea)
    save_json(PENDING, pending)
    return jsonify({"message": "Idea submitted for review!", "id": idea_id}), 201

@app.route("/ideas/pending", methods=["GET"])
def get_pending():
    token = request.headers.get("Authorization")
    if token != f"Bearer {ADMIN_TOKEN}":
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(load_json(PENDING))

@app.route("/ideas/approve/<int:idea_id>", methods=["POST"])
def approve(idea_id):
    token = request.headers.get("Authorization")
    if token != f"Bearer {ADMIN_TOKEN}":
        return jsonify({"error": "Unauthorized"}), 401

    pending = load_json(PENDING)
    approved = load_json(APPROVED)

    for idea in pending:
        if idea["id"] == idea_id:
            approved.append(idea)
            pending.remove(idea)
            save_json(APPROVED, approved)
            save_json(PENDING, pending)
            return jsonify({"message": "Idea approved!"}), 200

    return jsonify({"error": "Idea not found"}), 404

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)

