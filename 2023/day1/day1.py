import sys

digit_names = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}

sum = 0
for line in open(sys.argv[1], 'r'):
    line = line.strip()

    digits = []
    for i in range(len(line)):
        for name in digit_names:
            if line[i:].startswith(name):
                digits.append(digit_names[name])
    first_digit = digits[0]
    second_digit = digits[-1]
    number = 10 * first_digit + second_digit
    sum += number

print("SUM:")
print(sum)
