"""Second client: a command-line client that proves the server is client-agnostic."""
import requests

BASE = "http://127.0.0.1:5000/api/students"

def show(label, r):
    print(f"{label:<36} HTTP {r.status_code}  {r.text.strip()[:60]}")

if __name__ == "__main__":
    good = {"reg_no": "BIT/1234/22", "name": "Amon Kiptoo", "course": "BSc IT", "year": 3}
    r = requests.post(BASE, json=good)
    show("POST register student", r)
    sid = r.json()["id"]
    show("POST duplicate reg number", requests.post(BASE, json=good))
    show("POST invalid reg number", requests.post(BASE, json={**good, "reg_no": "123"}))
    show("GET all students", requests.get(BASE))
    show("PUT update year to 4", requests.put(f"{BASE}/{sid}", json={**good, "year": 4}))
    show("DELETE student", requests.delete(f"{BASE}/{sid}"))
    show("DELETE missing student", requests.delete(f"{BASE}/9999"))
