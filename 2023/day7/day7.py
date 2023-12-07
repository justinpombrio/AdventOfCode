import sys

CARD_ORDER = "AKQT98765432J"

def power(card):
    return len(CARD_ORDER) - CARD_ORDER.index(card)

def hand_type_with_wild(hand):
    best_type = 0
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
    counts = list(reversed(sorted(card_to_count.values())))
    if counts == [5]:
        return 5.0 # five of a kind
    elif counts == [4, 1]:
        return 4.0 # four of a kind
    elif counts == [3, 2]:
        return 3.5 # full house
    elif counts == [3, 1, 1]:
        return 3.0 # three of a kind
    elif counts == [2, 2, 1]:
        return 2.5 # two pair
    elif counts == [2, 1, 1, 1]:
        return 2.0 # one pair
    elif counts == [1, 1, 1, 1, 1]:
        return 1.0 # high card

def hand_score(hand):
    """Give a 'score' to hands, such that they sort correctly when sorted by their score"""
    return [hand_type_with_wild(hand)] + [power(card) for card in hand]

plays = []
for line in open(sys.argv[1], 'r'):
    [hand, bid] = line.strip().split()
    plays.append((hand, int(bid)))
plays.sort(key = lambda hand_and_bid: hand_score(hand_and_bid[0]))

print("Total:", sum([bid * (i + 1) for (i, (hand, bid)) in enumerate(plays)]))
