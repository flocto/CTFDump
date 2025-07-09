from PIL import Image
import numpy as np

data = open('oled-gadget.elf', 'rb').read()

start = 0x15c88
size = 2560

data = data[start:start + size]

def sh1108_bytes_to_image(data_bytes, width=128, height=160):
    """Convert SH1108 OLED byte data to PIL Image (128x160)"""
    if len(data_bytes) != 2560:
        raise ValueError(f"Expected 2560 bytes, got {len(data_bytes)}")
    
    # Create empty image array
    image_array = np.zeros((height, width), dtype=np.uint8)
    
    # SH1108 uses vertical byte mapping (8 pixels per byte, vertically arranged)
    for col in range(width):  # 128 columns
        for page in range(height // 8):  # 20 pages (160/8)
            byte_index = col + (page * width)
            byte_value = data_bytes[byte_index]
            
            # Extract 8 vertical pixels from this byte
            for bit in range(8):
                pixel_value = 255 if (byte_value & (1 << bit)) else 0
                row = (page * 8) + bit
                image_array[row, col] = pixel_value
    
    return Image.fromarray(image_array, mode='L')

img = sh1108_bytes_to_image(data)
# rot 90
img = img.rotate(90, expand=True)
img.save('oled-gadget.png')