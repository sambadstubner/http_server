def get_method_not_allowed():
        return """HTTP/1.0 405 Method Not Allowed
Content-Type: text/html
Content-Length: 174

<!DOCTYPE html>
<html>
<head>
    <title>405 Method Not Allowed</title>
</head>
<body>
    <h1>405 Method Not Allowed</h1>
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
        