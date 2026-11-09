"""SERVER ENTRY POINT: exposes the application layer over HTTP (JSON API)."""
from flask import Flask, jsonify, request, send_from_directory
import data_layer as db
import service_layer as svc

app = Flask(__name__, static_folder="static")
db.init()

def error(e):
    codes = {svc.ValidationError: 400, svc.NotFoundError: 404, svc.DuplicateError: 409}
    return jsonify(error=str(e)), codes[type(e)]

@app.get("/")
def index():
    return send_from_directory("static", "index.html")

@app.get("/api/students")
def get_students():
    return jsonify(svc.list_students())

@app.post("/api/students")
def create_student():
    try:
        new_id = svc.register_student(request.get_json(silent=True) or {})
    except (svc.ValidationError, svc.DuplicateError) as e:
        return error(e)
    return jsonify(id=new_id), 201

@app.put("/api/students/<int:student_id>")
def update_student(student_id):
    try:
        svc.edit_student(student_id, request.get_json(silent=True) or {})
    except (svc.ValidationError, svc.DuplicateError, svc.NotFoundError) as e:
        return error(e)
    return jsonify(id=student_id), 200

@app.delete("/api/students/<int:student_id>")
def delete_student(student_id):
    try:
        svc.remove_student(student_id)
    except svc.NotFoundError as e:
        return error(e)
    return "", 204

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
