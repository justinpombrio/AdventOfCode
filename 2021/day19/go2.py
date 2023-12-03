filename = "input.txt"

scans = []
scan = None
for line in open(filename, "r"):
    line = line.strip()
    if line == "":
        scans.append(scan)
    elif line.startswith("---"):
        scan = []
    else:
        parts = line.split(",")
        (x, y, z) = int(parts[0]), int(parts[1]), int(parts[2])
        scan.append((x, y, z))

for (i, scan) in enumerate(scans):
    print ""
    print "scan", i, scan
print ""

def orient(coord, orientation):
    (x, y, z) = coord
    (rotation, flipx, flipy, flipz) = orientation
    # rotate
    if rotation == 0: pass
    elif rotation == 1: (x, y, z) = (y, z, x)
    elif rotation == 2: (x, y, z) = (z, x, y)
    elif rotation == 3: (x, y, z) = (x, z, y)
    elif rotation == 4: (x, y, z) = (z, y, x)
    elif rotation == 5: (x, y, z) = (y, x, z)
    else: raise "bad"
    # flip
    return (x * flipx, y * flipy, z * flipz)

all_orientations = [(r, fx, fy, fz)
    for r in [0, 1, 2, 3, 4, 5]
    for fx in [-1, 1]
    for fy in [-1, 1]
    for fz in [-1, 1]]

class Frame:
    def __init__(self, location, orientation):
        self.location = location
        self.orientation = orientation

    def apply(self, rel_coord): # -> abs_coord
        (x, y, z) = rel_coord
        # orient
        (x, y, z) = orient((x, y, z), self.orientation)
        # offset
        (lx, ly, lz) = self.location
        (x, y, z) = (lx + x, ly + y, lz + z)
        return (x, y, z)

    def show(self):
        return str(self.location) + " / " + str(self.orientation)

# Find all frames such that rel_coord interpreted in that frame
# equals abs_coord. Formally:
#     frame.apply(rel_coord) = abs_coord
def possible_frames(abs_coord, rel_coord):
    frames = []
    for orientation in all_orientations:
        (x, y, z) = orient(rel_coord, orientation)
        (ax, ay, az) = abs_coord
        location = (ax - x, ay - y, az - z)
        frames.append(Frame(location, orientation))
    return frames

def confirm_frame(scanner1_frame, scans1, scanner2_frame, scans2):
    confirmation_count = 0
    for coord2 in scans2:
        abs_coord2 = scanner2_frame.apply(coord2)
        if abs_coord2 in scans1:
            confirmation_count += 1
    return confirmation_count >= 12

def find_frame(scanner1_frame, scans1, scans2):
    for abs_coord1 in scans1:
        for coord2 in scans2:
            for frame in possible_frames(abs_coord1, coord2):
                if confirm_frame(
                        scanner1_frame,
                        scans1,
                        frame,
                        scans2):
                    return frame
    return None

known_frames = [None for scanner in scans]
known_frames[0] = Frame((0, 0, 0), (0, 1, 1, 1))

considered = []
while None in known_frames:
    print ""
    print "known frames:"
    for (i, frame) in enumerate(known_frames):
        if frame is not None:
            print "  frame", i, frame.show()
    found = False
    for i in range(len(scans)):
        if found: break
        for j in range(len(scans)):
            if found: break
            if i == j: continue
            if known_frames[i] is None: continue
            if known_frames[j] is not None: continue
            if (i, j) in considered: continue
            print "considering", i, "->", j
            solved_scans_i = [
                known_frames[i].apply(scan) for scan in scans[i]
            ]
            frame = find_frame(
                      known_frames[i],
                      solved_scans_i,
                      scans[j])
            if frame is not None:
                print "found frame connection", i, "->", j, "!"
                known_frames[j] = frame
                found = True
            else:
                considered.append((i, j))

beacons = []
for (i, frame) in enumerate(known_frames):
    for rel_coord in scans[i]:
        abs_coord = frame.apply(rel_coord)
        if abs_coord not in beacons:
            beacons.append(abs_coord)
print "beacons"
for beacon in beacons:
    print "  ", beacon
print "num beacons", len(beacons)
