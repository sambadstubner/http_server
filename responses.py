def get_method_not_allowed():
        return """HTTP/1.0 400 Bad Request
Content-Type: text/html
Content-Length: 174

<!DOCTYPE html>
<html>
<head>
    <title>400 Bad Request</title>
</head>
<body>
    <h1>400 Bad Request</h1>
    <p>Your request is malformed or invalid.</p>
</body>
</html>
"""


def get_file_not_found():
        return """HTTP/1.0 404 Not Found
Content-Type: text/html
Content-Length: 186

<!DOCTYPE html>
<html>
<head>
    <title>404 Not Found</title>
</head>
<body>
    <h1>404 Not Found</h1>
    <p>The requested file could not be found on this server.</p>
</body>
</html>
"""
        