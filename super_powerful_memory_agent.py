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
    return hand_1,hand_2

#evaluate hand strength
def check_hands(hand):
    global RANKS
    rank_count={}
    for card in hand:
        rank=card[0]
        rank_count[rank]=rank_count.get(rank,0)+1

    if 3 in rank_count.values():#three of a kind
        ranki=[key for key,val in rank_count.items() if val==3][0]
        return "three of a kind",27+RANKS.index(ranki)
    elif 2 in rank_count.values():#pair
        ranki=[key for key,val in rank_count.items() if val==2][0]
        return "pair",14+RANKS.index(ranki)
    else:#Highe card
        high_card=max(hand,key=lambda card:RANKS.index(card[0]))
        return "high card",1+RANKS.index(high_card[0])

# Agent_1
def random_agent():
    return random.randrange(50,6,-1)

# Agent_2
def fixed_agent():
    return 25 # Always bid 25

# Agent_3
def reflex_agent(hand):
    hand_type,score=check_hands(hand)
    if hand_type=="three of a kind":
        return random.randint(30,50)#bid aggressively
    elif hand_type=="pair":
        return random.randint(15,30)#bid moderately
    else:
        return random.randint(5,15)#bid conservatively

# Enhanced Memory Agent
class SuperMemoryAgent:
    def __init__(self):
        self._opponents_bets = []
        self._opponent_type = None
        self._round_played = 0
        self._win_history = []
        self._confidence = 1.0  # Confidence starts at 1.0 (neutral)

    def _analyze_opponent(self):
        """Analyze opponent's betting behavior."""
        if len(set(self._opponents_bets)) == 1:  # Consistent bet
            self._opponent_type = "fixed"
        elif len(set(self._opponents_bets)) > 10:  # Randomized betting
            self._opponent_type = "random"
        else:  # Reflexive pattern
            self._opponent_type = "reflex_agent"

    def _adjust_confidence(self, win):
        """Adjust confidence level based on wins or losses."""
        if win:
            self._confidence = min(2.0, self._confidence + 0.1)  # Cap at 2.0
        else:
            self._confidence = max(0.5, self._confidence - 0.1)  # Minimum 0.5

    def make_bet(self, hand, last_opponent_bet, win=False):
        """Decide how much to bet."""
        if self._round_played > 5 and self._opponent_type is None:
            self._analyze_opponent()

        self._adjust_confidence(win)  # Update confidence after each round

        hand_type, hand_score = check_hands(hand)
        base_bet = 0

        if self._opponent_type == "fixed":
            if hand_score > 27:
                base_bet = last_opponent_bet + int(25 * self._confidence)
            elif hand_score > 14:
                base_bet = last_opponent_bet + random.randint(5, 30)
            else:
                base_bet = 5

        elif self._opponent_type == "random":
            if hand_score > 27:
                base_bet = random.randint(30, 50)
            elif hand_score > 14:
                base_bet = random.randint(10, 20)
            else:
                base_bet = 5

        elif self._opponent_type == "reflex_agent":
            if hand_score > 27:
                if 30 <= last_opponent_bet <= 50:
                    base_bet = last_opponent_bet - random.randint(10, 20)
                elif 15 <= last_opponent_bet <= 30:
                    base_bet = last_opponent_bet + random.randint(15, 20)
                else:
                    base_bet = random.randint(40, 50)
            elif hand_score > 14:
                if 30 <= last_opponent_bet <= 50:
                    base_bet = 5
                elif 15 <= last_opponent_bet <= 30:
                    base_bet = last_opponent_bet + random.randint(5, 10)
                else:
                    base_bet = random.randint(40, 50)
            else:
                base_bet = 5

        else:
            # If no clear opponent type, play conservatively like a reflex agent
            if hand_score > 27:
                base_bet = random.randint(30, 50)
            elif hand_score > 14:
                base_bet = random.randint(15, 30)
            else:
                base_bet = random.randint(5, 15)

        # Add a small bluffing factor
        if random.random() < 0.1:  # 10% chance to bluff
            base_bet += random.randint(10, 20)

        return base_bet

    def memory_update(self, opponent_bet, win):
        """Update memory and round history."""
        self._opponents_bets.append(opponent_bet)
        self._round_played += 1
        self._win_history.append(win)
def Lets_play(agent1, agent2):
    agent1_w = 0
    agent2_w = 0

    # Determine agent names and initialize instances if needed
    agent1_instance = agent1() if isinstance(agent1, type) else agent1
    agent2_instance = agent2() if isinstance(agent2, type) else agent2

    agent1_name = agent1_instance.__class__.__name__ if isinstance(agent1_instance, SuperMemoryAgent) else agent1.__name__
    agent2_name = agent2_instance.__class__.__name__ if isinstance(agent2_instance, SuperMemoryAgent) else agent2.__name__

    results = {agent1_name: 0, agent2_name: 0}

    for round_count in range(50):  # 50 rounds
        print(f"\n****** Round {round_count + 1} FIGHT! ******")

        # Phase 1: Card dealing
        hand1, hand2 = generate_2hands()
        print(f"{agent1_name} hand: {hand1}")
        print(f"{agent2_name} hand: {hand2}")

        # Evaluate hands
        _, hand1_score = check_hands(hand1)
        _, hand2_score = check_hands(hand2)

        # Phase 2: Bidding
        pot = 0
        last_opponent_bet = 0
        for phase in range(1, 4):  # 3 bidding phases
            # Determine bid1
            if isinstance(agent1_instance, SuperMemoryAgent):
                bid1 = agent1_instance.make_bet(hand1, last_opponent_bet)
            else:  # Callable function
                bid1 = agent1(hand1) if callable(agent1) and agent1.__code__.co_argcount > 0 else agent1()

            # Determine bid2
            if isinstance(agent2_instance, SuperMemoryAgent):
                bid2 = agent2_instance.make_bet(hand2, bid1)
            else:  # Callable function
                bid2 = agent2(hand2) if callable(agent2) and agent2.__code__.co_argcount > 0 else agent2()

            pot += bid1 + bid2
            last_opponent_bet = bid2

            if isinstance(agent1_instance, SuperMemoryAgent):
                agent1_instance.memory_update(last_opponent_bet, False)
            if isinstance(agent2_instance, SuperMemoryAgent):
                agent2_instance.memory_update(bid1, False)

            print(f"Bidding Phase {phase}: {agent1_name} bets {bid1}, {agent2_name} bets {bid2}")

        # Phase 3: Show hands
        if hand1_score > hand2_score:
            print(f"{agent1_name} wins the pot of ${pot}!")
            results[agent1_name] += pot
            agent1_w += 1
            if isinstance(agent1_instance, SuperMemoryAgent):
                agent1_instance.memory_update(last_opponent_bet, True)
            if isinstance(agent2_instance, SuperMemoryAgent):
                agent2_instance.memory_update(bid1, False)
        elif hand2_score > hand1_score:
            print(f"{agent2_name} wins the pot of ${pot}!")
            results[agent2_name] += pot
            agent2_w += 1
            if isinstance(agent1_instance, SuperMemoryAgent):
                agent1_instance.memory_update(last_opponent_bet, False)
            if isinstance(agent2_instance, SuperMemoryAgent):
                agent2_instance.memory_update(bid1, True)
        else:
            print(f"It's a tie! Pot of ${pot} is discarded.")

    # Final results
    print(f"\n**** Final Results ****")
    print(f"{agent1_name} total winnings: ${results[agent1_name]}")
    print(f"{agent2_name} total winnings: ${results[agent2_name]}")
    if results[agent1_name] > results[agent2_name]:
        print(f"*** THE GRAND WINNER IS {agent1_name} ***")
        return f"*** THE GRAND WINNER IS {agent1_name} *** $ {results[agent1_name]}with {agent1_w} round wins!"
    else:
        print(f"*** THE GRAND WINNER IS {agent2_name} ***")
        return f"*** THE GRAND WINNER IS {agent2_name} *** with $ {results[agent2_name]} {agent2_w} round wins!"


def main():

    print("\n*** Random Agent vs Fixed Agent ***")
    result = Lets_play(random_agent, fixed_agent)
    with open("Random_vs_Fixed.txt", "w", encoding='utf-8') as f:
        print(result, file=f)

    print("\n*** Reflex Agent vs Random Agent ***")
    result = Lets_play(reflex_agent, fixed_agent)
    with open("Reflex_vs_Random.txt", "w", encoding='utf-8') as f:
        print(result, file=f)

    print("\n*** Reflex Agent vs Fixed Agent ***")
    result = Lets_play(reflex_agent,fixed_agent)
    with open("Reflex_vs_Fixed.txt", "w", encoding='utf-8') as f:
        print(result, file=f)

    print("\n*** Memory Agent vs Random Agent ***")
    result = Lets_play(SuperMemoryAgent, random_agent)
    with open("SMemory_vs_Random.txt", "w", encoding='utf-8') as f:
        print(result, file=f)

    print("\n*** Memory Agent vs Fixed Agent ***")
    result=Lets_play(SuperMemoryAgent,fixed_agent)
    with open("SMemory_vs_Fixed.txt","w",encoding='utf-8') as f:
        print(result,file=f)

    print("\n*** Memory Agent vs reflex Agent ***")
    result = Lets_play(SuperMemoryAgent, reflex_agent)
    with open("SMemory_vs_Reflex.txt", "w", encoding='utf-8') as f:
        print(result, file=f)

if __name__=="__main__":
    main()