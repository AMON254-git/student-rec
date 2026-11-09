# Local Student Management System

A client-server application that manages student records. Clients (a browser page or a command-line script) send HTTP requests to a Flask server on `127.0.0.1:5000`. The server applies business rules then stores records in SQLite.

## Layered architecture

```
 CLIENT SIDE                          SERVER SIDE
┌──────────────────────┐   HTTP/JSON   ┌────────────────────────┐
│ PRESENTATION LAYER   │ ────────────► │ server.py (HTTP routes)│
│ static/index.html    │ ◄──────────── │          │             │
│ client_cli.py        │               │ APPLICATION LAYER      │
└──────────────────────┘               │ service_layer.py       │
                                       │ (validation, rules)    │
                                       │          │             │
                                       │ DATA LAYER             │
                                       │ data_layer.py + SQLite │
                                       └────────────────────────┘
```

| Layer | File | Responsibility |
|---|---|---|
| Presentation | `static/index.html`, `client_cli.py` | Collects student details, displays records, sends requests |
| Application | `server.py`, `service_layer.py` | Routes requests, validates reg numbers, blocks duplicates, maps errors to status codes |
| Data | `data_layer.py` | All SQL; stores records in `students.db` |

Each layer only talks to the one directly below it. The presentation layer never touches the database.

## Student record

| Field | Rule |
|---|---|
| `reg_no` | Required, unique, 2–8 alphanumeric groups separated by `/` or `-`, maximum 30 characters |
| `name` | Required, at least 2 characters |
| `course` | Required |
| `year` | Required, whole number from 1 to 4 |

## Run it

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python server.py                 # terminal 1, then open http://127.0.0.1:5000
python client_cli.py             # terminal 2 (second client)
```

## API

| Method | Endpoint | Success | Failure |
|---|---|---|---|
| GET | `/api/students` | 200 + list | n/a |
| POST | `/api/students` | 201 + id | 400 invalid data, 409 duplicate reg number |
| PUT | `/api/students/<id>` | 200 | 400, 404 not found, 409 duplicate |
| DELETE | `/api/students/<id>` | 204 | 404 not found |

## Evidence of successful communication

Output of `client_cli.py` against the running server:

```
POST register student                HTTP 201  {"id":1}
POST duplicate reg number            HTTP 409  {"error":"Reg number BIT/1234/22 already exists"}
POST invalid reg number              HTTP 400  {"error":""Reg number must be groups of letters or digits split by / or -"} 
GET all students                     HTTP 200  [{"course":"BSc IT",...
PUT update year to 4                 HTTP 200  {"id":1}
DELETE student                       HTTP 204
DELETE missing student               HTTP 404  {"error":"Student not found"}
```

Matching server log:

```
"POST /api/students HTTP/1.1" 201
"POST /api/students HTTP/1.1" 409
"POST /api/students HTTP/1.1" 400
"GET /api/students HTTP/1.1" 200
"PUT /api/students/1 HTTP/1.1" 200
"DELETE /api/students/1 HTTP/1.1" 204
"DELETE /api/students/9999 HTTP/1.1" 404
```

The browser page also shows a live request log under the table.
