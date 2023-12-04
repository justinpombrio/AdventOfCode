import sys

total_cards = 0
bonus_cards = [] # number of extra copies of future cards won
for (card_num, line) in enumerate(open(sys.argv[1], 'r')):
    # Number of copies of this card we gain
    copies = 1 if len(bonus_cards) == 0 else bonus_cards.pop(0) + 1
    total_cards += copies

    # Parse the card to get the number of matches
    sections = line.split(": ")
    parts = sections[1].split(" | ")
    winning = set(map(int, parts[0].split()))
    have = set(map(int, parts[1].split()))
    num_matches = len(winning & have)
    
    # Increase the number of bonus cards by 'copies' for the next 'num_matches' cards
    for i in range(num_matches):
        if i < len(bonus_cards):
            bonus_cards[i] += copies
        else:
            bonus_cards.append(copies)

    print("Card", card_num + 1, "score:", num_matches, "copies:", copies, "bonus:", bonus_cards)

print("\nSCORE:", total_cards)
