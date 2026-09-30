import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import sqlite3
from pathlib import Path

serverDir = Path(__file__).resolve().parent
schemaPath = serverDir / "database.sql"
databasePath = serverDir / "simplewall.db"
schema = schemaPath.read_text(encoding='utf-8')

class API(BaseHTTPRequestHandler):
    def do_GET(self):
        if (self.path == '/api/health'): # health check
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

            response = {"message": "Healthy and alive!!"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        elif (self.path == '/api/posts'): # get posts from the database
            connection = sqlite3.connect(databasePath)
            connection.row_factory = sqlite3.Row
            try:
                rows = connection.execute(
                    "SELECT id, content, createdAt, likes, numberofReports "
                    "FROM posts ORDER BY id DESC"
                ).fetchall()

                posts = []
                for row in rows:
                    posts.append(dict(row))
            finally:
                connection.close()

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(posts).encode('utf-8'))

        else: # return 404 if invalid API path
            self.send_response(404)
            self.end_headers()

    def do_POST(self): # handles POST requests
        if (self.path == '/api/posts'): # handles the posting of posts
            try:
                bodyLength = int(self.headers.get("Content-Length", "0"))
                if(bodyLength <= 0):
                    raise ValueError("Empty request body")

                body = self.rfile.read(bodyLength)
                data = json.loads(body)
            except(ValueError, UnicodeDecodeError):
                self.send_response(400)
                self.end_headers()
                return

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            response = {"message": "Request received!!!"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run(): # initialize database and run server on port 8000
    initializeDatabase()

    serverPort = 8000
    serverAddress = ('', serverPort)
    httpd = HTTPServer(serverAddress, API)
    print(f"API server running on port {serverPort}")
    httpd.serve_forever()

def initializeDatabase(): # initialize the database
    connection = sqlite3.connect(databasePath)
    try:
        connection.executescript(schema)
        connection.commit()
    finally:
        connection.close()


if __name__ == '__main__':
    run()