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

# Grid for Conway's Game of Life (7x10)
grid = bytearray(array_size)

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

def init_grid():
    """Initialize the grid with a simple pattern (e.g., glider)."""
    global grid
    # Clear the grid
    for i in range(array_size):
        grid[i] = 0
    # Set up a glider pattern at top-left
    grid[get_node_offset(1, 0)] = 1  # x=1, y=0
    grid[get_node_offset(2, 1)] = 1  # x=2, y=1
    grid[get_node_offset(0, 2)] = 1  # x=0, y=2
    grid[get_node_offset(1, 2)] = 1  # x=1, y=2
    grid[get_node_offset(2, 2)] = 1  # x=2, y=2

def count_neighbors(x, y):
    """Count live neighbors around a cell."""
    count = 0
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if dx == 0 and dy == 0:  # Skip the cell itself
                continue
            nx = (x + dx) % field_width   # Wrap around horizontally
            ny = (y + dy) % field_height  # Wrap around vertically
            count += grid[get_node_offset(nx, ny)]
    return count

def next_generation():
    """Compute the next generation based on Conway's rules."""
    global grid
    new_grid = bytearray(array_size)
    for y in range(field_height):
        for x in range(field_width):
            offset = get_node_offset(x, y)
            neighbors = count_neighbors(x, y)
            if grid[offset] == 1:  # Live cell
                if neighbors < 2 or neighbors > 3:
                    new_grid[offset] = 0  # Dies
                else:
                    new_grid[offset] = 1  # Lives
            else:  # Dead cell
                if neighbors == 3:
                    new_grid[offset] = 1  # Becomes alive
                else:
                    new_grid[offset] = 0  # Stays dead
    grid = new_grid

def draw_grid():
    """Draw the current grid state on the LED matrix."""
    overscan_fill(0)  # Clear the display
    for y in range(field_height):
        for x in range(field_width):
            if grid[get_node_offset(x, y)]:
                overscan_set_at(x, y, 255)

# Initialize the LED drivers
led_init()

# Set the LED current level (optional, adjust as needed)
led_current(0)  # Use 0, 1, 2, or 3 to adjust brightness

# Initialize the game grid
init_grid()

# Main loop
while True:
    gc.collect()
    draw_grid()       # Update the display with the current grid
    render()          # Send the display data to the LED drivers
    utime.sleep(0.5)  # Wait 0.5 seconds between generations
    next_generation() # Compute the next generation