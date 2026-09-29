import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import sqlite3
from pathlib import Path

class API(BaseHTTPRequestHandler):

    def do_GET(self):
        if (self.path == '/api/health'): # health check
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

            response = {"message": "Healthy and alive!!"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        elif (self.path == '/api/posts'): # get posts from the database(needs to be done)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

            response = {"message": "working on it"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else: # return 404 if invalid API path
            self.send_response(404)
            self.end_headers()

    def do_POST(self): # needs to be done
        if(True):
            print("under construction")

def run(): # initialize database and run server on port 8000
    initializeDatabase()

    serverPort = 8000
    serverAddress = ('', serverPort)
    httpd = HTTPServer(serverAddress, API)
    print(f"API server running on port {serverPort}")
    httpd.serve_forever()

def initializeDatabase(): # initialize the database
    serverDir = Path(__file__).resolve().parent
    schemaPath = serverDir / "database.sql"
    databasePath = serverDir / "simplewall.db"

    schema = schemaPath.read_text(encoding='utf-8')
    connection = sqlite3.connect(databasePath)

    try:
        connection.executescript(schema)
        connection.commit()
    finally:
        connection.close()


if __name__ == '__main__':
    run()