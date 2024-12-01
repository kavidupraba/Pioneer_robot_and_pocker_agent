import random

SUITS = ['s', 'h', 'd', 'c']  # spades, hearts, diamonds, clubs
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
DECK=[rank+suit for rank in RANKS for suit in SUITS]

#genarate random hands
def generate_2hands(number_of_cards=3):
    global DECK
    #deck=DECK[:] #same DECK.copy()
    deck=DECK.copy()
    random.shuffle(deck)
    hand_1=deck[:number_of_cards]
    hand_2=deck[number_of_cards:number_of_cards*2]
    print(hand_1)
    return hand_1,hand_2

#evaluate hand strength
def check_hands(hand):
    global RANKS
    rank_count={}
    for card in hand:
        rank=card[0]
        rank_count[rank]=rank_count.get(rank,0)+1

    high_card=max(hand,key=lambda card:RANKS.index(card[0]))
    return "high card",1+RANKS.index(high_card[0])

hand_1,hand_2=generate_2hands()
print(check_hands(hand_1))

