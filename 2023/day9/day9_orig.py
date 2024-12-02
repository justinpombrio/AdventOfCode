import sys

def extrapolate(seq):
    if all(map(lambda x: x == 0, seq)):
        return 0
    else:
        return seq[0] - extrapolate(differences(seq))

def differences(seq):
    return [seq[i + 1] - seq[i] for i in range(len(seq) - 1)]

seqs = []
for line in open(sys.argv[1], 'r'):
    seqs.append(list(map(int, line.strip().split())))

print(seqs)
total = 0
for seq in seqs:
    extra = extrapolate(seq)
    print(extra)
    total += extra

print("Total:", total)
