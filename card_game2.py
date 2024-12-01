import random

# Card deck and constants
SUITS = ['s', 'h', 'd', 'c']  # spades, hearts, diamonds, clubs
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
DECK = [rank + suit for rank in RANKS for suit in SUITS]

# Generate random hands
def generate_2hands(num_cards=3):
    deck = DECK[:]
    random.shuffle(deck)
    hand1 = deck[:num_cards]
    hand2 = deck[num_cards:num_cards * 2]
    return hand1, hand2

# Evaluate hand strength
def evaluate_hand(hand):
    rank_counts = {}
    for card in hand:
        rank = card[0]
        rank_counts[rank] = rank_counts.get(rank, 0) + 1

    if 3 in rank_counts.values():  # Three of a kind
        rank = [key for key, val in rank_counts.items() if val == 3][0]
        return "three_of_a_kind", 27 + RANKS.index(rank)
    elif 2 in rank_counts.values():  # Pair
        rank = [key for key, val in rank_counts.items() if val == 2][0]
        return "pair", 14 + RANKS.index(rank)
    else:  # High card
        high_card = max(hand, key=lambda card: RANKS.index(card[0]))
        return "high_card", 1 + RANKS.index(high_card[0])

# Agent 1: Random agent
def random_agent():
    return random.randint(0, 50)

# Agent 2: Fixed agent
def fixed_agent():
    return 25  # Always bids 25

# Agent 3: Reflex agent
def reflex_agent(hand):
    hand_type, hand_score = evaluate_hand(hand)
    if hand_type == "three_of_a_kind":
        return random.randint(30, 50)  # Aggressive bidding
    elif hand_type == "pair":
        return random.randint(15, 30)  # Moderate bidding
    else:
        return random.randint(5, 15)  # Conservative bidding

# Memory-based agent
class MemoryAgent:
    def __init__(self):
        self.opponent_bets = []  # Tracks opponent's past bets
        self.opponent_type = None  # Deduce the type of agent
        self.rounds_played = 0

    def analyze_opponent(self):
        """Analyze the opponent's betting history to deduce their type."""
        if len(set(self.opponent_bets)) == 1:  # Same bet every time
            self.opponent_type = "fixed"
        elif len(set(self.opponent_bets)) > 10:  # Highly varied bets
            self.opponent_type = "random"
        else:  # Bids appear linked to hand strength
            self.opponent_type = "reflex"

    def make_bet(self, hand, last_opponent_bet):
        """Decide how much to bet based on the opponent type and hand strength."""
        if self.rounds_played > 5 and not self.opponent_type:
            self.analyze_opponent()

        # Evaluate hand strength
        hand_type, hand_score = evaluate_hand(hand)

        if self.opponent_type == "fixed":
            if hand_score > 20:  # Strong hand
                return last_opponent_bet + 5  # Raise slightly
            else:
                return max(5, last_opponent_bet - 5)  # Bet conservatively

        elif self.opponent_type == "random":
            if hand_score > 25:  # Very strong hand
                return random.randint(30, 50)
            elif hand_score > 15:  # Moderate hand
                return random.randint(10, 20)
            else:
                return 5  # Conservative minimum bet

        elif self.opponent_type == "reflex":
            if hand_score > 25:  # Outbid reflex agent with strong hands
                return last_opponent_bet + 10
            else:  # Fold weak hands or bid minimally
                return 5

        # Default (undetermined opponent type)
        if hand_score > 25:
            return random.randint(30, 50)
        elif hand_score > 15:
            return random.randint(15, 30)
        else:
            return 5

    def update_memory(self, opponent_bet):
        """Update memory with the opponent's latest bet."""
        self.opponent_bets.append(opponent_bet)
        self.rounds_played += 1

# Poker game with memory-based agent
def play_poker_game_with_agents(agent1, agent2):
    results = {"Agent1": 0, "Agent2": 0}
    memory_agent_instance = MemoryAgent() if isinstance(agent1,type) else None

    for round_num in range(50):  # 50 rounds
        print(f"\n=== Round {round_num + 1} ===")

        # Phase 1: Card Dealing
        hand1, hand2 = generate_2hands()
        print(f"Agent 1's hand: {hand1}")
        print(f"Agent 2's hand: {hand2}")

        # Evaluate hands
        _, hand1_score = evaluate_hand(hand1)
        _, hand2_score = evaluate_hand(hand2)

        # Phase 2: Bidding
        pot = 0
        last_opponent_bet = 0
        for phase in range(1, 4):  # 3 bidding phases
            bid1 = agent1().make_bet(hand1, last_opponent_bet) if memory_agent_instance else agent1()
            bid2 = agent2(hand2) if agent2 == reflex_agent else agent2()
            pot += bid1 + bid2
            last_opponent_bet = bid2
            if memory_agent_instance:
                memory_agent_instance.update_memory(bid2)
            print(f"Bidding Phase {phase}: Agent 1 bets {bid1}, Agent 2 bets {bid2}")

        # Phase 3: Showdown
        if hand1_score > hand2_score:
            print(f"Agent 1 wins the pot of ${pot}!")
            results["Agent1"] += pot
        elif hand2_score > hand1_score:
            print(f"Agent 2 wins the pot of ${pot}!")
            results["Agent2"] += pot
        else:
            print(f"It's a tie! Pot of ${pot} is discarded.")

    # Final Results
    print("\n=== Final Results ===")
    print(f"Agent 1 total winnings: ${results['Agent1']}")
    print(f"Agent 2 total winnings: ${results['Agent2']}")

# Play the games
print("\n=== Memory Agent vs Fixed Agent ===")
play_poker_game_with_agents(MemoryAgent, fixed_agent)

print("\n=== Memory Agent vs Random Agent ===")
play_poker_game_with_agents(MemoryAgent, random_agent)

print("\n=== Memory Agent vs Reflex Agent ===")
play_poker_game_with_agents(MemoryAgent, reflex_agent)
