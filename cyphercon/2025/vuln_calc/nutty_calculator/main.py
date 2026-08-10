import socketserver

class NuttyCalculatorHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.sendall(b"Welcome to Nutty Calculator.\n")
        self.request.sendall(b"Enter arithmetic expressions:\n")
        while True:
            self.request.sendall(b"Nutty> ")
            expr = self.request.recv(1024).strip()
            if not expr:
                break
            try:
                result = eval(expr.decode('utf-8'))
                self.request.sendall(f"Result: {result}\n".encode())
            except Exception as e:
                self.request.sendall(f"Error: {e}\n".encode())

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 31337
    with socketserver.TCPServer((HOST, PORT), NuttyCalculatorHandler) as server:
        print(f"Nutty Calculator running on {HOST}:{PORT}")
        server.serve_forever()