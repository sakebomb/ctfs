import socket
import time

# Server configuration
SERVER_HOST = "192.168.8.2"
SERVER_PORT = 8001

def send_request(method, uri, headers=None):
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

def brew_tea(pot_id, tea_type, additions):
    """Brew a pot of tea with specified pot ID, type, and additions."""
    uri = f"/pot-{pot_id}/{tea_type}?{'&'.join(additions)}"
    headers = {
        "Content-Type": "message/teapot"
    }
    response = send_request("BREW", uri=uri, headers=headers)
    print(f"BREW response for pot-{pot_id}: {response}")

def stop_addition(pot_id, addition):
    """Send a WHEN request to stop a specific addition for a pot."""
    uri = f"/pot-{pot_id}/{addition}"
    response = send_request("WHEN", uri=uri)
    print(f"WHEN response for stopping {addition} in pot-{pot_id}: {response}")

def get_status():
    """Check the current status of the server."""
    response = send_request("GET", uri="/")
    print(f"GET response: {response}")

def when_ready():
    """Check when the brewing process is complete."""
    response = send_request("WHEN", uri="/")
    print(f"WHEN response: {response}")

# Demonstration
if __name__ == "__main__":
    tea_type = "oolong"
    additions = ["Cream", "Cream", "Sugar", "Sugar"]

    for pot_id in [1, 2]:
        print(f"\nBrewing pot-{pot_id} of Oolong tea with double cream and double sugar")
        brew_tea(pot_id, tea_type, additions)
        time.sleep(1)  # Wait 1 second before stopping creams
        print(f"Stopping each cream for pot-{pot_id}")
        stop_addition(pot_id, "Cream")  # Stop the first cream
        stop_addition(pot_id, "Cream")  # Stop the second cream
        print(f"Waiting for pot-{pot_id} to brew (5 seconds)")
        time.sleep(5)  # Wait 5 seconds for brewing to complete
        print(f"Checking status after pot-{pot_id}")
        get_status()

    # Optionally check when ready
    print("\nAsking when ready")
    when_ready()