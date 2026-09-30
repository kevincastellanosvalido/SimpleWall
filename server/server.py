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
            try: # validating that the content is all valid
                bodyLength = int(self.headers.get("Content-Length", "0"))
                if(bodyLength <= 0):
                    raise ValueError("Empty request body")

                body = self.rfile.read(bodyLength)
                data = json.loads(body)

                if (isinstance(data, dict)): # check that the parsed JSON is an object
                    print("Parsed JSON is an object!!")
                else:
                    raise ValueError(f"Valid JSON, but {type(data).__name__}, not object")

                content = data.get("content")

                if(isinstance(content, str)): # check that the content is a string
                    print("Success! Content is a string!")
                    content = content.strip()
                else:
                    raise ValueError(f"Error! Content is not a string, it's a {type(data).__name__}")

                if(len(content) <= 400 and len(content) > 0): # check that the string length is appropriate
                    print("Content is long enough!")
                else:
                    if(len(content) > 400):
                        raise ValueError(f"Length must not exceed 400 characters! String is {len(content) - 400} over!")
                    else:
                        raise ValueError("Length must be more than 0 characters!")          
                
            except(ValueError, UnicodeDecodeError): # if the content is not valid, error 400
                self.send_response(400)
                self.end_headers()
                return

            connection = sqlite3.connect(databasePath) # open DB connection
            try: # insert content into DB
                cursor = connection.execute("INSERT INTO posts (content) VALUES (?)", (content,))
                connection.commit()
            finally:
                connection.close()

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