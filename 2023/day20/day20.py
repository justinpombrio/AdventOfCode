import sys

modules = {}
for line in open(sys.argv[1], 'r'):
    src, dst = line.strip().split(" -> ")
    destinations = list(dst.split(", "))
    if src[0] == "%":
        modules[src[1:]] = ("%", destinations)
    elif src[0] == "&":
        modules[src[1:]] = ("&", destinations)
    else:
        modules["broadcast"] = ("broadcast", destinations)

flip_flop_state = {}
conj_state = {}

for mod, (op, _) in modules.items():
    if op == "%":
        flip_flop_state[mod] = 0
    elif op == "&":
        conj_state[mod] = {}

for mod, (op, dests) in modules.items():
    for dest in dests:
        if dest in conj_state:
            conj_state[dest][mod] = 0

def exec(times):
    low_count = 0
    high_count = 0
    for i in range(times):
        print("iter", i)
        pulses = [("button", 0, "broadcast")]
        while len(pulses) > 0:
            (src, pulse, mod) = pulses.pop(0)
            #print("Pulse:", src, pulse, mod)
            if mod == "rx" and pulse == 0:
                print("done!", i)
                sys.exit(1)
            if pulse == 0:
                low_count += 1
            else:
                high_count += 1
            if mod not in modules:
                #print("  missing module:", mod)
                continue
            (op, dests) = modules[mod]
            if op == "broadcast":
                for dest in dests:
                    pulses.append((mod, pulse, dest))
            elif op == "%" and pulse == 0:
                new_pulse = 1 - flip_flop_state[mod]
                flip_flop_state[mod] = 1 - flip_flop_state[mod]
                for dest in dests:
                    pulses.append((mod, new_pulse, dest))
            elif op == "&":
                conj_state[mod][src] = pulse
                if all([p == 1 for p in conj_state[mod].values()]):
                    new_pulse = 0
                else:
                    new_pulse = 1
                for dest in dests:
                    pulses.append((mod, new_pulse, dest))

    print("low", low_count, "high", high_count)
    return low_count * high_count

for module_name in modules:
    print(module_name, modules[module_name])

print()

product = exec(100000000)
print("Pulse product:", product)
