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
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()
    new_id = events[-1].id + 1 if events else 1
    new_event = Event(id=new_id, title=data.get("title"))
    events.append(new_event)
    return jsonify(new_event.to_dict()), 201

@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = next((e for e in events if e.id == event_id), None)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    data = request.get_json()
    if "title" in data:
        event.title = data["title"]
        
    return jsonify(event.to_dict()), 200

@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = next((e for e in events if e.id == event_id), None)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    events.remove(event)
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)
