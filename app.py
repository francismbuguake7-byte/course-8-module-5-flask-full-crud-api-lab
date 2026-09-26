from flask import Flask, jsonify, request

app = Flask(__name__)


# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


# In-memory "database"
events = [Event(1, "Tech Meetup"), Event(2, "Python Workshop")]


# TODO: Task 1 - Define the Problem
# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or "title" not in data:
        return jsonify({"error": "The title field is required"}), 400

    event_id = max((event.id for event in events), default=0) + 1
    event = Event(event_id, data["title"])
    events.append(event)
    return jsonify(event.to_dict()), 201


# TODO: Task 1 - Define the Problem
# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or "title" not in data:
        return jsonify({"error": "The title field is required"}), 400

    for event in events:
        if event.id == event_id:
            event.title = data["title"]
            return jsonify(event.to_dict()), 200

    return jsonify({"error": "Event not found"}), 404


# TODO: Task 1 - Define the Problem
# Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    for event in events:
        if event.id == event_id:
            events.remove(event)
            return "", 204

    return jsonify({"error": "Event not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
