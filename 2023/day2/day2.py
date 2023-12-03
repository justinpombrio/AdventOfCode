import sys

sum = 0
for line in open(sys.argv[1], 'r'):
    line = line.strip()

    sections = line.split(": ")
    game_id = int(sections[0].split(" ")[1])

    # Determine minimum number of each color required to see the results we saw
    required_colors = {"red": 0, "green": 0, "blue": 0}
    for reveal in sections[1].split("; "):
        for draw in reveal.split(", "):
            num, color = draw.split(" ")
            required_colors[color] = max(required_colors[color], int(num))

    # Calculate power
    power = 1
    for color, num in required_colors.items():
        power *= num
    sum += power

    print(game_id, required_colors, power)

print()
print("SUM:")
print(sum)
