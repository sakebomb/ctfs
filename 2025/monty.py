import paho.mqtt.client as mqtt
from meshtastic import mqtt_pb2, portnums_pb2
import subprocess

# MQTT settings
BROKER = "localhost"
PORT = 1883
TOPIC = "msh/#"
USERNAME = "meshdev"
PASSWORD = "large4cats"

# Meshtastic settings
MESHTASTIC_PORT = "/dev/ttyUSB0"  # Replace with your actual port

# Chatbot configuration
questions = [
    "What... is your name?",
    "What... is your quest?",
    "What... is the air-speed velocity of an unladen swallow?"
]
user_state = {}  # Dictionary to track node states: node_id -> state

def send_message(text, dest_node):
    """Send a message to a specific node using the meshtastic command-line tool.
    
    Note: For direct messages to a specific destination, the --ch-index option is not used.
    """
    hex_id = f"{dest_node:08x}"  # Convert integer node ID to 8-digit hex string
    cmd = [
        "meshtastic",
        "--port", MESHTASTIC_PORT,
        "--sendtext", text,
        "--dest", hex_id
    ]
    subprocess.run(cmd, capture_output=True, text=True)
    print(f"Sent to {hex_id}: {text}")

def get_node_id_from_topic(topic):
    """Extract the node ID from the MQTT topic."""
    parts = topic.split('/')
    if len(parts) >= 5 and parts[4].startswith('!'):
        hex_id = parts[4][1:]  # Remove the '!' prefix
        try:
            return int(hex_id, 16)  # Convert hex string to integer
        except ValueError:
            return None
    return None

def on_connect(client, userdata, flags, rc):
    """Callback for when the client connects to the MQTT broker."""
    print(f"Connected with result code {rc}")
    client.subscribe(TOPIC)
    print("Waiting for 'bridgekeeper' on channel 1")

def on_message(client, userdata, msg):
    """Callback for when a message is received from the MQTT broker."""
    # Parse the ServiceEnvelope from the message payload
    envelope = mqtt_pb2.ServiceEnvelope()
    try:
        envelope.ParseFromString(msg.payload)
    except Exception as e:
        print(f"Failed to parse payload: {e}")
        return

    # Ensure the envelope contains a packet
    if not envelope.HasField("packet"):
        print("No packet in envelope")
        return

    packet = envelope.packet

    # Ensure the packet has a decoded field
    if not packet.HasField("decoded"):
        print("No decoded field")
        return

    # Check if it's a text message
    if packet.decoded.portnum != portnums_pb2.PortNum.TEXT_MESSAGE_APP:
        return  # Ignore non-text messages

    # Extract node ID from the topic
    node_id = get_node_id_from_topic(msg.topic)
    if node_id is None:
        print(f"Invalid topic: {msg.topic}")
        return

    # Decode and process the message text
    message_text = packet.decoded.payload.decode('utf-8').lower().strip()
    print(f"Received from {node_id}: {message_text}")

    # State machine logic
    if "bridgekeeper" in message_text:
        user_state[node_id] = "waiting_ask_me"
        send_message(
            "Stop. Who would cross the Bridge of Death must answer me these questions three, ere the other side he see.",
            node_id
        )
    elif node_id in user_state:
        state = user_state[node_id]
        if state == "waiting_ask_me":
            if "ask me" in message_text:
                user_state[node_id] = "question_0"
                send_message(questions[0], node_id)
        elif state == "question_0":
            if message_text:
                user_state[node_id] = "question_1"
                send_message(questions[1], node_id)
            else:
                send_message("Please provide an answer.", node_id)
        elif state == "question_1":
            if message_text:
                user_state[node_id] = "question_2"
                send_message(questions[2], node_id)
            else:
                send_message("Please provide an answer.", node_id)
        elif state == "question_2":
            if "african or european" in message_text:
                send_message("flag{d0_u_m3sh_m3}", node_id)
                del user_state[node_id]  # Interaction complete
            else:
                send_message("Wrong! Let's start again.", node_id)
                user_state[node_id] = "waiting_ask_me"

# Set up MQTT client
client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker and start the loop
client.connect(BROKER, PORT, 60)
client.loop_forever()