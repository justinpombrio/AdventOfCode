import sys

area = 0
left_right = 0
trench_len = 0
for line in open(sys.argv[1], 'r'):
    (_part1_dir, _part1_len, code) = line.strip().split()
    length = int(code[2:7], 16)
    direction = "RDLU"[int(code[7])]
    trench_len += length
    for _ in range(length):
        if direction == "R":
            left_right += 1
        elif direction == "L":
            left_right -= 1
        elif direction == "U":
            area += left_right
        elif direction == "D":
            area -= left_right

area = abs(area)
area_of_trench = trench_len // 2 + 1
total_area = area + area_of_trench
print("Total area:", total_area)
