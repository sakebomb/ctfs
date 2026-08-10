import machine
import rp2
import utime
import gc

# I2C setup
i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0), freq=100000)

# Define global variables
field_width = 7
field_height = 10
array_size = field_width * field_height

overscan = bytearray(array_size)

# Gamma correction table for brightness mapping
gama_64 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 29, 32, 35, 38, 41, 44, 47, 50, 53, 57, 61, 65, 69, 73, 77, 81, 85, 89, 94, 99, 104, 109, 114, 119, 124, 129, 134, 140, 146, 152, 158, 164, 170, 176, 182, 188, 195, 202, 209, 216, 223, 230, 237, 244, 251, 255]

# LED driver mappings
chip_60 = [66, 59, 52, 45, 38, 65, 58, 51, 44, 37, 30, 23, 16, 9, 2, 64, 57, 50, 43, 36, 29, 22, 15, 8, 1, 63, 56, 49, 42, 35, 28, 21, 14, 7, 0]
chip_63 = [6, 13, 20, 27, 34, 41, 48, 55, 62, 69, 5, 12, 19, 26, 33, 40, 47, 54, 61, 68, 4, 11, 18, 25, 32, 39, 46, 53, 60, 67, 3, 10, 17, 24, 31]

buffer_60 = bytearray(35)
buffer_63 = bytearray(35)

# Simple 7x10 font for characters (example patterns)
font = {
    'f': [
        [0,0,0,0,0,0,0],
        [0,1,1,1,1,1,0],
        [0,1,0,0,0,0,0],
        [0,1,0,0,0,0,0],
        [0,1,1,1,0,0,0],
        [0,1,0,0,0,0,0],
        [0,1,0,0,0,0,0],
        [0,1,0,0,0,0,0],
        [0,1,0,0,0,0,0],
        [0,0,0,0,0,0,0]
    ],
    'l': [
        [0,0,0,0,0,0,0],
        [0,1,0,0,0,0,0],
        [0,1,0,0,0,0,0],
        [0,1,0,0,0,0,0],
        [0,1,0,0,0,0,0],
        [0,1,0,0,0,0,0],
        [0,1,0,0,0,0,0],
        [0,1,0,0,0,0,0],
        [0,1,1,1,1,1,0],
        [0,0,0,0,0,0,0]
    ],
    'a': [
        [0,0,0,0,0,0,0],
        [0,0,1,1,1,0,0],
        [0,1,0,0,0,1,0],
        [0,1,0,0,0,1,0],
        [0,1,0,0,0,1,0],
        [0,1,1,1,1,1,0],
        [0,1,0,0,0,1,0],
        [0,1,0,0,0,1,0],
        [0,1,0,0,0,1,0],
        [0,0,0,0,0,0,0]
    ],
    'g': [
        [0,0,0,0,0,0,0],
        [0,0,1,1,1,0,0],
        [0,1,0,0,0,1,0],
        [0,1,0,0,0,0,0],
        [0,1,0,0,0,0,0],
        [0,1,0,1,1,1,0],
        [0,1,0,0,0,1,0],
        [0,1,0,0,0,1,0],
        [0,0,1,1,1,0,0],
        [0,0,0,0,0,0,0]
    ],
    '{': [
        [0,0,0,0,0,0,0],
        [0,0,0,1,1,0,0],
        [0,0,1,0,0,0,0],
        [0,0,1,0,0,0,0],
        [0,1,1,0,0,0,0],
        [0,1,1,0,0,0,0],
        [0,0,1,0,0,0,0],
        [0,0,1,0,0,0,0],
        [0,0,0,1,1,0,0],
        [0,0,0,0,0,0,0]
    ],
    '}': [
        [0,0,0,0,0,0,0],
        [0,0,1,1,0,0,0],
        [0,0,0,0,1,0,0],
        [0,0,0,0,1,0,0],
        [0,0,0,0,1,1,0],
        [0,0,0,0,1,1,0],
        [0,0,0,0,1,0,0],
        [0,0,0,0,1,0,0],
        [0,0,1,1,0,0,0],
        [0,0,0,0,0,0,0]
    ],
    'I': [
        [0,0,0,0,0,0,0],
        [0,1,1,1,1,1,0],
        [0,0,0,1,0,0,0],
        [0,0,0,1,0,0,0],
        [0,0,0,1,0,0,0],
        [0,0,0,1,0,0,0],
        [0,0,0,1,0,0,0],
        [0,0,0,1,0,0,0],
        [0,1,1,1,1,1,0],
        [0,0,0,0,0,0,0]
    ],
    ' ': [
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0]
    ],
    '*': [
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,1,0,0,0,1,0],
        [1,1,1,0,1,1,1],
        [1,1,1,1,1,1,1],
        [0,1,1,1,1,1,0],
        [0,0,1,1,1,0,0],
        [0,0,0,1,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0]
    ],
    'D': [
        [0,0,0,0,0,0,0],
        [0,1,1,1,0,0,0],
        [0,1,0,0,1,0,0],
        [0,1,0,0,0,1,0],
        [0,1,0,0,0,1,0],
        [0,1,0,0,0,1,0],
        [0,1,0,0,0,1,0],
        [0,1,0,0,1,0,0],
        [0,1,1,1,0,0,0],
        [0,0,0,0,0,0,0]
    ],
    'i': [
        [0,0,0,0,0,0,0],
        [0,0,0,1,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,1,0,0,0],
        [0,0,0,1,0,0,0],
        [0,0,0,1,0,0,0],
        [0,0,0,1,0,0,0],
        [0,0,0,1,0,0,0],
        [0,0,0,1,0,0,0],
        [0,0,0,0,0,0,0]
    ],
    'c': [
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,1,1,1,0,0],
        [0,1,0,0,0,0,0],
        [0,1,0,0,0,0,0],
        [0,1,0,0,0,0,0],
        [0,0,1,1,1,0,0],
        [0,0,0,0,0,0,0]
    ],
    'k': [
        [0,0,0,0,0,0,0],
        [0,1,0,0,0,0,0],
        [0,1,0,0,0,0,0],
        [0,1,0,0,1,0,0],
        [0,1,0,1,0,0,0],
        [0,1,1,0,0,0,0],
        [0,1,1,0,0,0,0],
        [0,1,0,1,0,0,0],
        [0,1,0,0,1,0,0],
        [0,0,0,0,0,0,0]
    ],
    's': [
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,1,1,1,0,0],
        [0,1,0,0,0,0,0],
        [0,0,1,0,0,0,0],
        [0,0,0,1,0,0,0],
        [0,0,0,0,1,0,0],
        [0,1,1,1,0,0,0],
        [0,0,0,0,0,0,0]
    ]
}

def led_init():
    """Initialize the LED drivers."""
    i2c.writeto_mem(0x3C, 0x4F, b'\x00')
    i2c.writeto_mem(0x3C, 0x00, b'\x01')
    i2c.writeto_mem(0x3F, 0x4F, b'\x00')
    i2c.writeto_mem(0x3F, 0x00, b'\x01')
    for i in range(0, 36):
        i2c.writeto_mem(0x3C, 0x26 + i, b'\x07')
        i2c.writeto_mem(0x3F, 0x26 + i, b'\x07')
    i2c.writeto_mem(0x3C, 0x25, b'\x00')
    i2c.writeto_mem(0x3F, 0x25, b'\x00')

def led_current(level):
    """Set the current level for the LEDs."""
    if level == 0:
        for i in range(0, 36):
            i2c.writeto_mem(0x3C, 0x26 + i, b'\x07')
            i2c.writeto_mem(0x3F, 0x26 + i, b'\x07')
    elif level == 1:
        for i in range(0, 36):
            i2c.writeto_mem(0x3C, 0x26 + i, b'\x05')
            i2c.writeto_mem(0x3F, 0x26 + i, b'\x05')
    elif level == 2:
        for i in range(0, 36):
            i2c.writeto_mem(0x3C, 0x26 + i, b'\x03')
            i2c.writeto_mem(0x3F, 0x26 + i, b'\x03')
    elif level == 3:
        for i in range(0, 36):
            i2c.writeto_mem(0x3C, 0x26 + i, b'\x01')
            i2c.writeto_mem(0x3F, 0x26 + i, b'\x01')
    i2c.writeto_mem(0x3C, 0x25, b'\x00')
    i2c.writeto_mem(0x3F, 0x25, b'\x00')

def render():
    """Render the overscan array to the LED drivers."""
    global buffer_60, buffer_63, overscan
    for i in range(0, 35):
        buffer_60[i] = overscan[chip_60[i]]
        buffer_63[i] = overscan[chip_63[i]]
    i2c.writeto_mem(60, 2, buffer_60)
    i2c.writeto_mem(63, 2, buffer_63)
    i2c.writeto_mem(0x3C, 0x25, b'\x00')
    i2c.writeto_mem(0x3F, 0x25, b'\x00')

def overscan_fill(value):
    """Fill the overscan array with a specific value."""
    global overscan
    temp = int(value / 4)
    for i in range(0, array_size):
        overscan[i] = gama_64[temp]

def overscan_set_at(x, y, value):
    """Set a specific LED in the overscan array."""
    global overscan
    temp = int(value / 4)
    node_offset = get_node_offset(x, y)
    overscan[node_offset] = gama_64[temp]

def get_node_offset(x, y):
    """Calculate the offset in the overscan array for a given (x, y)."""
    global field_width
    return (y * field_width) + x

def draw_char(char):
    """Draw a single character on the LED matrix."""
    overscan_fill(0)  # Clear the display
    if char in font:
        pattern = font[char]
        for y in range(10):
            for x in range(7):
                if pattern[y][x]:
                    overscan_set_at(x, y, 255)

# Initialize the LED drivers
led_init()

# Set the LED current level (optional, adjust as needed)
led_current(0)  # Use 0, 1, 2, or 3 to adjust brightness

# String to display
display_string = "flag{I * Dicks}"

# Main loop
while True:
    gc.collect()
    for char in display_string:
        draw_char(char)
        render()
        utime.sleep(1.5)  # Wait 1.5 seconds between characters