from PIL import Image
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="Simple jpg -> terminal art processor")
parser.add_argument("-f", type=str, required=True, help="Provide input jpg filepath")
parser.add_argument("--cutoff", action="store_true", help="lowers brightness of left 1/3rd")
parser.add_argument("--inverse", action="store_true", help="inverts brightness")
parser.add_argument("--padding", type=float, required=False, default=0.0, help="shifts image to right by a factor of arg times its width")
parser.add_argument("--resize", type=float, required=False, default=1.0, help="multiplicative image dimensions resizer")
parser.add_argument("--colour", type=int, required=False, default=36, help="set text colour using ascii escape code integer values e.g. 36 = cyan")

args = parser.parse_args()

#DIR = "/home/hphipps_/terminal_art"
IMAGE = args.f
print("processing", IMAGE)
ASCIIs = ' `^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'
MAX_BRIGHTNESS = 255
RESIZE=args.resize

image = Image.open(IMAGE)
image = image.resize((int(RESIZE*image.width), int(RESIZE*image.height)))
pixels = image.load()

not_rgb = False
try:
    r,g,b = pixels[0,0]
except:
    print("not rgb")
    not_rgb = True

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
    if args.inverse:
        gamma = 0.2    
    else: gamma = 7 # < 1 brightens highlights, darkens shadows
    boosted = norm ** gamma
    # Rescale to 0–255
    return int(boosted * 255)

method = contrast

if not_rgb == False:
    matrix = np.zeros((image.height, image.width), dtype=np.float64)
    for i in range(image.height):
        for j in range(image.width):
            if i == 0 or i == image.height:
                matrix[i,j] = 255
            else:
                matrix[i,j] = method(pixels[j,i])
else: matrix = np.array(image)

matrix = np.pad(matrix, pad_width=((0,0), (int(args.padding*image.width), 0)), mode="constant", constant_values=0.0) 

if args.inverse:
    matrix = 255 - matrix

def map_val_to_ascii(val):
    space = MAX_BRIGHTNESS/len(ASCIIs)
    char = ASCIIs[min(int(val // space), 64)]
    #if char == "`":
    #    char = " "
    return char

ascii_matrix = np.zeros((np.shape(matrix)[0], np.shape(matrix)[1]), dtype=str)
for i in range(np.shape(matrix)[0]):
    for j in range(np.shape(matrix)[1]):
        if i == 0 or i == np.shape(matrix)[0]-1:
            char = map_val_to_ascii(5)
        else:
            if args.cutoff and j < 0.3*np.shape(matrix)[1]:
                if args.inverse:
                     val = 0
                else: val = 0.1*matrix[i,j]
                char = map_val_to_ascii(val)
            else: 
                char = f"\033[{args.colour}m{map_val_to_ascii(matrix[i,j])}\033[0m"
        print(char, end="")
        print(char, end="")
        print(char, end="")
        ascii_matrix[i,j] = char
    print("")

