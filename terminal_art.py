from PIL import Image
import numpy as np

IMAGE = "/home/hphipps_/terminal_art/burial_crop.jpg"
ASCIIs = ' `^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'
MAX_BRIGHTNESS = 255

image = Image.open(IMAGE)
image = image.resize((int(0.1*image.width), int(0.1*image.height)))
pixels = image.load()

def average(rgb):
    r, g, b = rgb
    return (r+g+b)/3

def lightness(rgb):
    return (max(rgb) + min(rgb)) /2

def luminosity(rgb):
    r, g, b = rgb
    return 0.21*r + 0.72*g + 0.07*b

def contrast(rgb):
    r, g, b = rgb
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    # Normalize to 0–1
    norm = luminance / 255.0
    # Apply gamma correction to boost contrast
    gamma =  7 # < 1 brightens highlights, darkens shadows
    boosted = norm ** gamma
    # Rescale to 0–255
    return int(boosted * 255)

method = contrast

matrix = np.zeros((image.height, image.width), dtype=np.float64)
for i in range(image.height):
    for j in range(image.width):
        if i == 0 or i == image.height:
            matrix[i,j] = 255
        else:
            matrix[i,j] = method(pixels[j,i])

def map_val_to_ascii(val):
    space = MAX_BRIGHTNESS/len(ASCIIs)
    char = ASCIIs[min(int(val // space), 64)]
    #if char == "`":
    #    char = " "
    return char

ascii_matrix = np.zeros((image.height, image.width), dtype=str)
for i in range(image.height):
    for j in range(image.width):
        if i == 0 or i == image.height-1:
            char = map_val_to_ascii(5)
        else:
            if j < 0.3*image.width:
                char = map_val_to_ascii(0.1*matrix[i,j])
            else: 
                char = f"\033[36m{map_val_to_ascii(matrix[i,j])}\033[0m"
        print(char, end="")
        print(char, end="")
        print(char, end="")
        ascii_matrix[i,j] = char
    print("")
