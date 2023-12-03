import sys

filename = "input.txt"

def tobit(ch):
    if ch == "#": return 1
    elif ch == ".": return 0
    else: raise "oops"

in_image = False
image = []
for line in open(filename, "r"):
    line = line.strip()
    if line == "":
        in_image = True
        continue
    if in_image:
        image.append([tobit(ch) for ch in line])
    else:
        algorithm = [tobit(ch) for ch in line]

def tonumber(binary):
    n = 0
    for bit in binary:
        n *= 2
        n += bit
    return n

def expand(image):
    width = len(image[0])
    return ([[0 for _ in range(width + 2)]]
            + [[0] + row + [0] for row in image]
            + [[0 for _ in range(width + 2)]])

def expand_n(image, n):
    result = image
    for _ in range(n):
        result = expand(result)
    return result

def shrink(image):
    width = len(image[0])
    height = len(image)
    return [[image[x+1][y+1] for x in range(width-2)]
            for y in range(height-2)]

def shrink_n(image, n):
    result = image
    for _ in range(n):
        result = shrink(result)
    return result

def neighbors(x, y):
    return [(x-1,y-1), (x,y-1), (x+1,y-1),
            (x-1,y  ), (x,y  ), (x+1,y  ),
            (x-1,y+1), (x,y+1), (x+1,y+1)]

def get_pixel_number(image, x, y):
    bits = [image[y][x] for (x, y) in neighbors(x, y)]
    return tonumber(bits)

def enhance(image):
    width = len(image[0])
    height = len(image)
    new_image = [[0 for _ in range(width)]
                 for _ in range(height)]
    for x in range(1, width-1):
        for y in range(1, height-1):
            new_pixel = algorithm[get_pixel_number(image, x, y)]
            new_image[y][x] = new_pixel
    return expand(new_image)

def print_img(image):
    for row in image:
        for bit in row:
            if bit == 0: sys.stdout.write(".")
            else: sys.stdout.write("#")
        print ""

def pixel_count(image):
    count = 0
    for row in image:
        for bit in row:
            if bit == 1: count += 1
    return count

EXPANSION_SIZE = 200

image = expand(expand(image))
image = expand_n(image, EXPANSION_SIZE)

print "algorithm", algorithm, len(algorithm)
print "image:"
print_img(image)
print "pixel count", pixel_count(image)

for i in range(50):
    print ""
    print "step", i
    image = enhance(image)
    print "image:"
    print_img(image)
    print "pixel count", pixel_count(image)

print "final shrinking"
image = shrink_n(image, EXPANSION_SIZE)
print "image:"
print_img(image)
print "pixel count", pixel_count(image)

