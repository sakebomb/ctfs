import paho.mqtt.client as mqtt
from meshtastic import mqtt_pb2, portnums_pb2  # Use portnums_pb2 for PortNum
from Crypto.Cipher import AES
import base64
import subprocess

# MQTT settings
BROKER = "localhost"
PORT = 1883
TOPIC = "msh/#"
USERNAME = "meshdev"
PASSWORD = "large4cats"
KEY = ""  # Replace with your base64-encoded AES key if encryption is used

# Meshtastic settings
MESHTASTIC_PORT = "/dev/ttyUSB0"  # Replace with your device's serial port
CHANNEL_INDEX = 1  # Replace with the index of the "cyphercon" channel

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    print(f"Topic: {msg.topic}")
    
    envelope = mqtt_pb2.ServiceEnvelope()
    envelope.ParseFromString(msg.payload)
    packet = envelope.packet
    
    if packet.HasField("encrypted"):
        key_bytes = base64.b64decode(KEY)
        nonce = packet.id.to_bytes(8, "little") + packet.from_.to_bytes(8, "little")
        cipher = AES.new(key_bytes, AES.MODE_CTR, nonce=nonce)
        decrypted = cipher.decrypt(packet.encrypted)
        
        data = portnums_pb2.Data()
        data.ParseFromString(decrypted)
        packet.decoded.CopyFrom(data)
    
    if packet.HasField("decoded"):
        if packet.decoded.portnum == portnums_pb2.PortNum.TEXT_MESSAGE_APP:
            message_text = packet.decoded.payload.decode('utf-8')
            print(f"Text: {message_text}")
            # Check for "hello little friend" in any case combination
            if "hello little friend" in message_text.lower() or "hello my little friend" in message_text.lower():
                # Execute the meshtastic CLI command to send the flag
                try:
                    cmd = [
                        "meshtastic",
                        "--port", MESHTASTIC_PORT,
                        "--sendtext", "flag{wh3r3_my_m3ssh13s_4t}",
                        "--ch-index", str(CHANNEL_INDEX)
                    ]
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    print("Meshtastic command output:", result.stdout)
                    if result.stderr:
                        print("Meshtastic command error:", result.stderr)
                except Exception as e:
                    print(f"Failed to send Meshtastic message: {e}")
        else:
            print(f"Port: {packet.decoded.portnum}, Payload: {packet.decoded.payload}")

client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_forever()