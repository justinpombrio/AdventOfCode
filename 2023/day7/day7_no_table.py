import sys

CARD_ORDER = "AKQT98765432J"

def power(card):
    return len(CARD_ORDER) - CARD_ORDER.index(card)

def hand_type_with_wild(hand):
    best_type = []
    for card in CARD_ORDER:
        possible_type = hand_type_without_wild(hand.replace("J", card))
        best_type = max(best_type, possible_type)
    return best_type

def hand_type_without_wild(hand):
    card_to_count = {}
    for card in hand:
        if card not in card_to_count:
            card_to_count[card] = 0
        card_to_count[card] += 1
    return list(reversed(sorted(card_to_count.values())))

def hand_score(hand):
    """Give a 'score' to hands, such that they sort correctly when sorted by their score"""
    return [hand_type_with_wild(hand)] + [power(card) for card in hand]

plays = []
for line in open(sys.argv[1], 'r'):
    [hand, bid] = line.strip().split()
    plays.append((hand, int(bid)))
plays.sort(key = lambda hand_and_bid: hand_score(hand_and_bid[0]))

print("Total:", sum([bid * (i + 1) for (i, (hand, bid)) in enumerate(plays)]))
