import socket
import time

SERVER_HOST = "172.20.2.2"
SERVER_PORT = 8000
DEFAULT_COFFEE_URI = f"coffee://{SERVER_HOST}/pot"


def send_request(method, uri=DEFAULT_COFFEE_URI, headers=None):
    """Send a request to the server and return the response."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        request = f"{method} {uri} HTCPCP/1.0\r\n"
        if headers:
            for key, value in headers.items():
                request += f"{key}: {value}\r\n"
        request += "\r\n"
        client_socket.send(request.encode("utf-8"))
        response = client_socket.recv(1024).decode("utf-8")
        return response
    finally:
        client_socket.close()


def brew_coffee(additions=None, language="english"):
    """Attempt to brew coffee, handling the 418 teapot error if it occurs."""
    # Map language to scheme (simplified from server)
    scheme_map = {
        "english": "coffee",
        "esperanto": "kafo",
        "french": "caf%C3%A8",
        "german": "%4Baffee",
    }
    scheme = scheme_map.get(language, "coffee")
    uri = f"{scheme}://{SERVER_HOST}/pot"
    if additions:
        uri += "?" + "&".join(additions)  # Add additions to query string
    response = send_request("BREW", uri=uri)
    print(f"BREW response: {response}")

    # Check for 418 I'm a teapot status
    if "418 I'm a teapot" in response:
        print("Error: This pot is a teapot and cannot brew coffee.")
        return None, None  # Return None to indicate failure
    return scheme, additions  # Return scheme and additions for successful brew


def get_status(scheme="coffee"):
    """Check the status of the coffee pot."""
    uri = f"{scheme}://{SERVER_HOST}/pot-1"
    response = send_request("GET", uri=uri)
    print(f"GET response: {response}")


def when_ready(scheme="coffee", additive=None):
    """Stop an additive or check readiness."""
    uri = f"{scheme}://{SERVER_HOST}/pot-1"
    if additive:
        uri += f"/{additive}"
    response = send_request("WHEN", uri=uri)
    print(f"WHEN response: {response}")


# Demonstration
if __name__ == "__main__":
    print("Brewing coffee in Esperanto with Cream")
    scheme, additions = brew_coffee(["Cream"], language="esperanto")

    if scheme is not None:  # Proceed only if brewing was successful
        print("\nChecking status after 2 seconds")
        time.sleep(2)
        get_status(scheme)

        print("\nStopping Cream with WHEN after 1 more second")
        time.sleep(1)
        when_ready(scheme, "Cream")

        print("\nChecking status again")
        time.sleep(1)
        get_status(scheme)

        print("\nWaiting for completion (5 more seconds)")
        time.sleep(5)
        get_status(scheme)
    else:
        print("Cannot proceed with brewing as the pot is a teapot.")
