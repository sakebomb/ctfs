import socket
import threading
import time
from urllib.parse import urlparse
import argparse
import random

# Global configuration for Safe header (default: False)
INCLUDE_SAFE_HEADER = False

class CoffeePot:
    def __init__(self, is_teapot=False):
        self.state = "idle"  # idle, brewing, ready
        self.brewing_start_time = None
        self.brewing_duration = 5  # Shortened for demonstration
        self.language = "english"
        self.additions = []  # List of additions with type and parameters
        self.active_additions = {}  # Tracks which additions are being "poured"
        self.beverage_type = None  # Will be "coffee" or a tea type
        self.is_teapot = is_teapot  # Flag to indicate if this is a teapot
        self.lock = threading.Lock()
        self.available_teas = ["darjeeling", "earl-grey", "peppermint"]  # Available tea types
        # Mapping of schemes to languages (simplified)
        self.scheme_to_language = {
            "koffie": "afrikaans",                  # Afrikaans, Dutch
            "q%C3%A6hv%C3%A6": "azerbaijani",       # Azerbaijani
            "%D9%82%D9%87%D9%88%D8%A9": "arabic",  # Arabic
            "akeita": "basque",                    # Basque
            "koffee": "bengali",                   # Bengali
            "kahva": "bosnian",                    # Bosnian
            "kafe": "czech",                      # Bulgarian, Czech
            "caf%C3%A8": "french",                # Catalan, French, Galician
            "%E5%92%96%E5%95%A1": "chinese",      # Chinese
            "kava": "croatian",                    # Croatian
            "k%C3%A1va": "czech",                 # Czech
            "kaffe": "danish",                    # Danish, Norwegian, Swedish
            "coffee": "english",                  # English
            "kafo": "esperanto",                  # Esperanto
            "kohv": "estonian",                   # Estonian
            "kahvi": "finnish",                   # Finnish
            "%4Baffee": "german",                 # German
            "%CE%BA%CE%B1%CF%86%CE%AD": "greek", # Greek
            "%E0%A4%95%E0%A5%8C%E0%A4%AB%E0%A5%80": "hindi", # Hindi
            "%E3%82%B3%E3%83%BC%E3%83%92%E3%83%BC": "japanese", # Japanese
            "%EC%BB%A4%ED%94%BC": "korean",      # Korean
            "%D0%BA%D0%BE%D1%84%D0%B5": "russian", # Russian
            "%E0%B8%81%E0%B8%B2%E0%B9%81%E0%B8%9F": "thai" # Thai
        }
        # Language-specific responses (translated "Coffee brewed successfully!")
        self.flags = {
            "afrikaans": "Koffie suksesvol gebrou!",
            "azerbaijani": "Qəhvə uğurla dəmləndi!",
            "arabic": "تم تحضير القهوة بنجاح!",
            "basque": "Kafea arrakastaz prestatu da!",
            "bengali": "কফি সফলভাবে তৈরি হয়েছে!",
            "bosnian": "Kafa je uspešno skuvana!",
            "czech": "Káva úspěšně připravena!",  # Same for Bulgarian, Czech
            "french": "Café infusé avec succès!",  # Same for Catalan, French, Galician
            "chinese": "咖啡冲泡成功！",
            "croatian": "Kava je uspješno skuhana!",
            "danish": "Kaffe brygget succesfuldt!",  # Same for Danish, Norwegian, Swedish
            "english": "Coffee brewed successfully!",
            "esperanto": "Kafo sukcese pretigita!",
            "estonian": "Kohv edukalt valmis!",
            "finnish": "Kahvi keitetty onnistuneesti!",
            "german": "Kaffee erfolgreich gebrüht!",
            "greek": "Ο καφές παρασκευάστηκε με επιτυχία!",
            "hindi": "कॉफ़ी सफलतापूर्वक तैयार की गई!",
            "japanese": "コーヒーが正常に淹れられました！",
            "korean": "커피가 성공적으로 추출되었습니다!",
            "russian": "Кофе успешно заварен!",
            "thai": "กาแฟชงสำเร็จแล้ว!"
        }
        # Valid addition types from RFC 2324 and RFC 7168
        self.valid_additions = {
            "milk": {"Cream", "Half-and-half", "Whole-milk", "Part-Skim", "Skim", "Non-Dairy"},
            "syrup": {"Vanilla", "Almond", "Raspberry", "Chocolate"},
            "sweetener": {"Sugar", "Saccharin", "Aspartame", "Stevia"},
            "alcohol": {"Whisky", "Rum", "Kahlua", "Aquavit"},
            "spice": {"Cinnamon", "Nutmeg", "Cardamom"},
            "sugar": {"Sugar", "Xylitol", "Stevia"}
        }

    def start_brewing(self, language, beverage_type, additions):
        with self.lock:
            if self.state != "idle":
                return False
            self.state = "brewing"
            self.brewing_start_time = time.time()
            self.language = self.scheme_to_language.get(language, "english")
            self.beverage_type = beverage_type
            self.additions = additions
            self.active_additions = {add["type"]: True for add in additions}
            threading.Timer(self.brewing_duration, self.finish_brewing).start()
            return True

    def finish_brewing(self):
        with self.lock:
            self.state = "ready"
            self.active_additions.clear()

    def stop_addition(self, addition_type):
        with self.lock:
            if self.state != "brewing":
                return "Coffee pot is not brewing", False
            if addition_type not in self.active_additions:
                return f"No active {addition_type} being added", False
            if not self.active_additions.get(addition_type, False):
                return f"{addition_type} already stopped", False
            self.active_additions[addition_type] = False
            return f"Stopped adding {addition_type}", True

    def get_status(self):
        with self.lock:
            if self.state == "brewing":
                elapsed = time.time() - self.brewing_start_time
                if elapsed >= self.brewing_duration:
                    self.state = "ready"
            device_type = "teapot" if self.is_teapot else "coffee pot"
            if self.state == "ready":
                if self.beverage_type == "coffee":
                    message = self.flags.get(self.language, "Unknown language")
                else:
                    message = f"{self.beverage_type.capitalize()} tea brewed successfully!"
                if self.additions:
                    additions_str = ", ".join([add["type"] for add in self.additions])
                    message += f" with {additions_str}"
                return f"{device_type.capitalize()} status: {self.state}\n{message}"
            active_str = f" (Active additions: {', '.join([k for k, v in self.active_additions.items() if v])})" if self.state == "brewing" else ""
            return f"{device_type.capitalize()} status: {self.state}{active_str}"

def parse_additions(query, valid_additions):
    if not query:
        return []
    additions = []
    for addition_str in query.split("&"):
        parts = addition_str.split(";")
        if not parts or not parts[0]:
            continue
        add_type = parts[0]
        is_valid = False
        for category, types in valid_additions.items():
            if add_type in types:
                is_valid = True
                break
        if not is_valid:
            return None
        addition = {"type": add_type}
        for param in parts[1:]:
            if "=" in param:
                key, value = param.split("=", 1)
                addition[key] = value
        additions.append(addition)
    return additions

def get_available_additions(valid_additions):
    additions_list = []
    for category, types in valid_additions.items():
        additions_list.extend(types)
    return "Available additions: " + ", ".join(sorted(additions_list))

def generate_propfind_response(coffee_pot):
    additions_xml = "".join([f'<addition type="{add["type"]}" active="{"true" if coffee_pot.active_additions.get(add["type"], False) else "false"}" />' for add in coffee_pot.additions])
    device_type = "teapot" if coffee_pot.is_teapot else "coffee pot"
    xml = f"""
    <propfind xmlns="DAV:">
      <prop>
        <pot-id>{coffee_pot.pot_id}</pot-id>
        <device-type>{device_type}</device-type>
        <state>{coffee_pot.state}</state>
        <language>{coffee_pot.language}</language>
        <additions>{additions_xml}</additions>
      </prop>
    </propfind>
    """
    return xml.strip()

def handle_client(client_socket, coffee_pots, coffee_pots_lock):
    try:
        request = client_socket.recv(1024).decode("utf-8").strip()
        if not request:
            return

        # Parse request headers
        request_lines = request.split("\r\n")
        first_line = request_lines[0]
        headers = {}
        for line in request_lines[1:]:
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip()] = value.strip()

        content_type = headers.get('Content-Type', 'message/coffeepot')
        parts = first_line.split()
        if len(parts) < 2:
            return
        method, uri = parts[0], parts[1]

        parsed_uri = urlparse(uri)
        scheme = parsed_uri.scheme
        path = parsed_uri.path or "/"
        query = parsed_uri.query

        # Handle pot designator and tea type
        path_parts = path.strip('/').split('/')
        if path_parts and path_parts[0].startswith('pot-'):
            try:
                pot_id = int(path_parts[0][4:])
                if pot_id < 1:
                    raise ValueError
            except ValueError:
                response = "HTCPCP/1.0 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nInvalid pot-designator"
                client_socket.send(response.encode("utf-8"))
                return
        elif path_parts and path_parts[0] == 'pot':
            pot_id = 1
        else:
            pot_id = 1  # Default to pot-1

        tea_type = None
        if len(path_parts) > 1 and path_parts[0].startswith('pot-'):
            tea_type = path_parts[1]

        valid_additions = coffee_pots[pot_id].valid_additions if pot_id in coffee_pots else CoffeePot().valid_additions
        additions = parse_additions(query, valid_additions)

        with coffee_pots_lock:
            if pot_id not in coffee_pots:
                is_teapot = random.random() < 0.05
                coffee_pots[pot_id] = CoffeePot(is_teapot=is_teapot)
            coffee_pot = coffee_pots[pot_id]

        coffee_pot.pot_id = pot_id

        if method in ("BREW", "POST"):
            if content_type == 'message/teapot':
                if tea_type is None:  # e.g., "/", "/pot-1"
                    available_teas = coffee_pot.available_teas
                    alternates_entries = [f'{{"/pot-{pot_id}/{tea}" {{type message/teapot}}}}' for tea in available_teas]
                    alternates = ', '.join(alternates_entries)
                    response = f"HTCPCP/1.0 300 Multiple Choices\r\nAlternates: {alternates}\r\n\r\n"
                    client_socket.send(response.encode("utf-8"))
                    return
                else:  # e.g., "/pot-1/darjeeling"
                    if tea_type not in coffee_pot.available_teas:
                        response = "HTCPCP/1.0 404 Not Found\r\nContent-Type: text/plain\r\n\r\nTea type not available"
                        client_socket.send(response.encode("utf-8"))
                        return
                    beverage_type = tea_type
                    if coffee_pot.start_brewing(scheme, beverage_type, additions):
                        response_body = "Brewing started"
                        safe_header = "Safe: yes" if INCLUDE_SAFE_HEADER else ""
                    else:
                        response_body = "Already brewing"
                        safe_header = "Safe: no" if INCLUDE_SAFE_HEADER else ""
            elif content_type == 'message/coffeepot':
                if tea_type is not None:
                    response = "HTCPCP/1.0 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nCannot brew coffee with tea type specified"
                    client_socket.send(response.encode("utf-8"))
                    return
                if coffee_pot.is_teapot:
                    response = "HTCPCP/1.0 418 I'm a teapot\r\nContent-Type: text/plain\r\n\r\nThis is a teapot, not a coffee pot!"
                    client_socket.send(response.encode("utf-8"))
                    return
                beverage_type = "coffee"
                if coffee_pot.start_brewing(scheme, beverage_type, additions):
                    response_body = "Brewing started"
                    safe_header = "Safe: yes" if INCLUDE_SAFE_HEADER else ""
                else:
                    response_body = "Already brewing"
                    safe_header = "Safe: no" if INCLUDE_SAFE_HEADER else ""
            else:
                response_body = "Unsupported Content-Type"
                safe_header = "Safe: no" if INCLUDE_SAFE_HEADER else ""
        elif method == "GET":
            status = coffee_pot.get_status()
            response_body = status
            safe_header = "Safe: yes" if INCLUDE_SAFE_HEADER else ""
        elif method == "PROPFIND":
            xml_response = generate_propfind_response(coffee_pot)
            response = f"HTCPCP/1.0 200 OK\r\nContent-Type: application/xml\r\n\r\n{xml_response}"
            client_socket.send(response.encode("utf-8"))
            return
        elif method == "WHEN":
            additive = tea_type if tea_type else (query.split("=")[0] if query else "")
            if not additive:
                response_body = "No additive specified for WHEN"
                safe_header = "Safe: no" if INCLUDE_SAFE_HEADER else ""
            else:
                message, success = coffee_pot.stop_addition(additive)
                response_body = message
                safe_header = "Safe: yes" if success and INCLUDE_SAFE_HEADER else "Safe: no" if INCLUDE_SAFE_HEADER else ""
        else:
            response_body = "Method not supported"
            safe_header = "Safe: no" if INCLUDE_SAFE_HEADER else ""

        headers = "Content-Type: text/plain"
        if safe_header:
            headers += f"\r\n{safe_header}"

        response = f"HTCPCP/1.0 200 OK\r\n{headers}\r\n\r\n{response_body}"
        client_socket.send(response.encode("utf-8"))
    finally:
        client_socket.close()

def run_server(host="127.0.0.1", port=8001, include_safe_header=False):
    global INCLUDE_SAFE_HEADER
    INCLUDE_SAFE_HEADER = include_safe_header
    coffee_pots = {}
    coffee_pots_lock = threading.Lock()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Serving HTCPCP on {host}:{port} {'with Safe header' if include_safe_header else 'without Safe header'}")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            threading.Thread(target=handle_client, args=(client_socket, coffee_pots, coffee_pots_lock)).start()
    finally:
        server_socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HTCPCP Socket Server")
    parser.add_argument("--host", default="127.0.0.1", help="Server host")
    parser.add_argument("--port", type=int, default=8001, help="Server port")
    parser.add_argument("--safe-header", action="store_true", help="Include Safe header in responses")
    args = parser.parse_args()
    run_server(host=args.host, port=args.port, include_safe_header=args.safe_header)