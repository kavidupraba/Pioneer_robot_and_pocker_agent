import random
import os

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
    return random.randrange(50,4,-1)
    #return random.randint(5,50)

# Agent_2
def fixed_agent():
    return 25 # Always bid 25

# Agent_3
def reflex_agent(hand):
    hand_type,score=check_hands(hand)
    if hand_type=="three of a kind":
        return random.randint(30,50)#bid aggressively
        #return 50
    elif hand_type=="pair":
        return random.randint(15,30)#bid moderately
        #return 25
    else:
        return random.randint(5,15)#bid conservatively
        #return 5

# Agent_3
class Memory_agent:
    def __init__(self):

        self._opponents_bets={"three_of_a_kind":[],"pair":[],"high_hand":[]}
        self._opponent_type=None
        self._round_played=0

    def _Analize_opponent(self):
        memory_ranges = {
            "three_of_a_kind": range(30, 51),
            "pair": range(15, 31),
            "high_hand": range(5, 16),
        }

        # Check if the opponent is fixed
        all_bets = (
                self._opponents_bets["three_of_a_kind"]
                + self._opponents_bets["pair"]
                + self._opponents_bets["high_hand"]
        )
        if len(set(all_bets)) == 1:  # Same bet every time
            self._opponent_type = "fixed"
            return

        # Check if the opponent is reflex
        for hand_type, valid_range in memory_ranges.items():
            bets = self._opponents_bets[hand_type]
            if bets and not all(bet in valid_range for bet in bets):
                break
        else:
            self._opponent_type = "reflex_agent"
            return

        # If neither fixed nor reflex, classify as random
        self._opponent_type = "random"


        #self._opponent_type = "reflex_agent"

        '''
        elif len(set(self._opponents_bets))>10:#bet is always different
            self._opponent_type="random"
        else:
            self._opponent_type="reflex_agent"
        '''

    def __make_bet__(self,hand,last_opponent_bet):
        #Decide how much to bet on opponent type and hand strength
        if self._round_played>5 and self._opponent_type is None:
            self._Analize_opponent()

        hand_type,hand_score=check_hands(hand)
        if self._opponent_type=="fixed":
            if hand_score>=27:
                if hand_score==39:
                  return last_opponent_bet+25
                else:
                    return last_opponent_bet+10
                #return 50
            elif hand_score>=14:
                return last_opponent_bet+random.randint(5,20)
            else:
                return 5

        elif self._opponent_type=="random":
            if hand_score>=27:
                if hand_score == 39:
                    return last_opponent_bet + 25
                else:
                   return random.randint(15,30)
            elif hand_score>=14:
                return random.randint(10,20)
            else:
                return 5

        elif self._opponent_type=="reflex_agent":
            if hand_score>=27:
                if hand_score==39:
                    return 50
                elif 30<=last_opponent_bet<=50:
                    return last_opponent_bet-random.randint(10,20)
                  #return random.randint(10,30)
                elif 15<=last_opponent_bet<=30:
                    return last_opponent_bet+random.randint(15,20)
                else:
                    return random.randint(40,50)
                    #return 50
            elif hand_score>=14:
                if 30<=last_opponent_bet<=50:
                    return 5
                elif 15<=last_opponent_bet<=30:
                    return last_opponent_bet+random.randint(5,10)
                   # we bet agrisivly because of in the end of trhe game the victory is calculated from all the money we bet in game
                else:
                    return random.randint(40,50)
                    # return 50
            else:
                return 5
        #if we don't have the opponent type play like reflex agent  we don't read apponent bet because this can be
        #misleading (if fix or random agent playing we can't tell what is their hand strength acording to their bet
        if hand_score>=27:
            return random.randint(30,50)
        elif hand_score>=14:
            return random.randint(15,30)
        else:
            return random.randint(5,15)

    def __memory_update__(self, opponent_bet, op_hand):
        hand_type_mapping = {
            "three of a kind": "three_of_a_kind",
            "pair": "pair",
            "high card": "high_hand",
        }
        if op_hand in hand_type_mapping:
            self._opponents_bets[hand_type_mapping[op_hand]].append(opponent_bet)
        self._round_played += 1

    def __getstate__(self):
        return self._opponent_type


def Lets_play(agent1,agent2):
    agent1_w=0
    agent2_w=0
    #agent1_name = agent1.__class__.__name__ if isinstance(agent1, type) else agent1.__name__
    #agent2_name = agent2.__class__.__name__ if isinstance(agent2, type) else agent2.__name__
    agent1_name = agent1.__class__.__name__ if isinstance(agent1, Memory_agent) else agent1.__name__
    agent2_name = agent2.__class__.__name__ if isinstance(agent2, Memory_agent) else agent2.__name__

    if agent1_name==agent2_name:
        agent1_name=agent2_name+"1"
        agent2_name=agent2_name+"2"

    results = {agent1_name: 0, agent2_name: 0}
    Memory_agent_instance1=Memory_agent() if isinstance(agent1,type) else None
    Memory_agent_instance2=Memory_agent()if isinstance(agent2,type) else None

    for round_count in range(50):#50 rounds like said in the book
        print(f"\n ******Round: {round_count+1} FIGHT!******")

        #phase 1 card dealing
        hand1,hand2=generate_2hands()
        print(f"{agent1_name} hand {hand1}")
        print(f"{agent2_name} hand {hand2}")

        #evaluate hands
        hand_type1,hand1_score=check_hands(hand1)
        hand_type2,hand2_score=check_hands(hand2)

        #phase 2 bidding
        pot=0
        last_opponent_bet=0
        for phase in range(1,4):#3 bidding phase
            if Memory_agent_instance1:
                bid1=Memory_agent_instance1.__make_bet__(hand1,last_opponent_bet)
                bid2=agent2(hand2)if agent2==reflex_agent else agent2()
                #bid2=reflex_agent(hand2) if agent2==reflex_agent else agent2()
                pot+=(bid1+bid2)
                last_opponent_bet=bid2
            elif Memory_agent_instance2:
                bid1=agent1(hand1)if agent1==reflex_agent else agent1()
                bid2=Memory_agent_instance2.__make_bet__(hand2,last_opponent_bet)
                pot+=(bid1+bid2)
                last_opponent_bet=bid1
            else:
                bid1=agent1(hand1)if agent1==reflex_agent else agent1()
                bid2=agent2(hand2)if agent2==reflex_agent else agent2()
                pot+=(bid1+bid2)
            if Memory_agent_instance1 or Memory_agent_instance2:
                if Memory_agent_instance1:
                   Memory_agent_instance1.__memory_update__(last_opponent_bet,hand_type2)
                else:
                   Memory_agent_instance2.__memory_update__(last_opponent_bet,hand_type1)
            print(f"Bidding Phase {phase}: {agent1_name} bets {bid1}, {agent2_name} bets {bid2}")

        #phase 3 show hands
        if hand1_score>hand2_score:
            print(f"{agent1_name} wins the pot of ${pot}!")
            results[agent1_name]+=pot
            agent1_w+=1
        elif hand2_score>hand1_score:
            print(f"{agent2_name} wins the pot of ${pot}!")
            results[agent2_name]+=pot
            agent2_w+=1
        else:
            print(f"It's a tie! Pot of ${pot} is discarded.")

    #Final result
    print(f"\n**** Final Results ****")
    print(f"{agent1_name} total winnings: ${results[agent1_name]}")
    print(f"{agent2_name} total winnings: ${results[agent2_name]}")
    if results[agent1_name]>results[agent2_name]:
        print(f"***THE GRAND WINNER IS {agent1_name}***")
        if Memory_agent_instance1:
          result =Memory_agent_instance1.__getstate__()
          return f"***THE GRAND WINNER IS {agent1_name}***, {results[agent1_name]} rounds wins {agent1_w} against: {result} it's wins  {agent2_w} rounds and won ${results[agent2_name]}"
        else:
           return f"***THE GRAND WINNER IS {agent1_name}***, {results[agent1_name]} rounds wins {agent1_w} against: {agent2_name} it's wins {agent2_w} rounds and won ${results[agent2_name]}"
    else:
        print(f"***THE GRAND WINNER IS {agent2_name}***")
        if Memory_agent_instance2:
           result=Memory_agent_instance2.__getstate__()
           return f"***THE GRAND WINNER IS {agent2_name}***, {results[agent2_name]} rounds wins {agent2_w} against: {result} it's wins {agent1_w} rounds and won ${results[agent1_name]}"
        else:
            return f"***THE GRAND WINNER IS {agent2_name}***, {results[agent2_name]} rounds wins {agent2_w} against: {agent1_name} it's wins {agent1_w} rounds and won ${results[agent1_name]}"


def main():

    #random vs random
    if os.path.lexists(r"/A_I_course\lab1_code\Random_vs_Random.txt"):
        print("\n*** Random Agent vs Random Agent ***")
        result = Lets_play(random_agent, random_agent)
        with open("Random_vs_Random.txt", "a", encoding='utf-8') as f:
            print(result, file=f)
    else:
        print("\n*** Random Agent vs Random Agent ***")
        result = Lets_play(random_agent, random_agent)
        with open("Random_vs_Random.txt", "x", encoding='utf-8') as f:
            print(result, file=f)

    #fixed vs fixed
    if os.path.lexists(r"/A_I_course\lab1_code\Fixed_vs_Fixed.txt"):
        print("\n*** Fixed Agent vs Fixed Agent ***")
        result = Lets_play(fixed_agent, fixed_agent)
        with open("Fixed_vs_Fixed.txt", "a", encoding='utf-8') as f:
            print(result, file=f)
    else:
        print("\n*** Fixed Agent vs Fixed Agent ***")
        result = Lets_play(fixed_agent, fixed_agent)
        with open("Fixed_vs_Fixed.txt", "x", encoding='utf-8') as f:
            print(result, file=f)

    #Reflex vs Reflex
    if os.path.lexists(r"/A_I_course\lab1_code\Reflex_vs_Reflex.txt"):
        print("\n*** Reflex Agent vs Reflex Agent ***")
        result = Lets_play(reflex_agent, reflex_agent)
        with open("Reflex_vs_Reflex.txt", "a", encoding='utf-8') as f:
            print(result, file=f)
    else:
        print("\n*** Reflex Agent vs Reflex Agent ***")
        result = Lets_play(reflex_agent, reflex_agent)
        with open("Reflex_vs_Reflex.txt", "x", encoding='utf-8') as f:
            print(result, file=f)


    #Random vs Fixed
    if os.path.lexists(r"/A_I_course\lab1_code\Random_vs_Fixed.txt"):
        print("\n*** Random Agent vs Fixed Agent ***")
        result = Lets_play(random_agent, fixed_agent)
        with open("Random_vs_Fixed.txt", "a", encoding='utf-8') as f:
            print(result, file=f)
    else:
        print("\n*** Random Agent vs Fixed Agent ***")
        result = Lets_play(random_agent, fixed_agent)
        with open("Random_vs_Fixed.txt", "x", encoding='utf-8') as f:
            print(result, file=f)

    #Reflex vs Random
    if os.path.lexists(r"/A_I_course\lab1_code\Reflex_vs_Random.txt"):
        print("\n*** Reflex Agent vs Random Agent ***")
        result = Lets_play(reflex_agent, fixed_agent)
        with open("Reflex_vs_Random.txt", "a", encoding='utf-8') as f:
            print(result, file=f)
    else:
        print("\n*** Reflex Agent vs Random Agent ***")
        result = Lets_play(reflex_agent, fixed_agent)
        with open("Reflex_vs_Random.txt", "x", encoding='utf-8') as f:
            print(result, file=f)

    #Reflex vs Fixed
    if os.path.lexists(r"/A_I_course\lab1_code\Reflex_vs_Fixed.txt"):
        print("\n*** Reflex Agent vs Fixed Agent ***")
        result = Lets_play(reflex_agent,fixed_agent)
        with open("Reflex_vs_Fixed.txt", "a", encoding='utf-8') as f:
            print(result, file=f)
    else:
        print("\n*** Reflex Agent vs Fixed Agent ***")
        result = Lets_play(reflex_agent, fixed_agent)
        with open("Reflex_vs_Fixed.txt", "x", encoding='utf-8') as f:
            print(result, file=f)

    #Memory vs Random
    if os.path.lexists(r"/A_I_course\lab1_code\Memory_vs_Random.txt"):
        print("\n*** Memory Agent vs Random Agent ***")
        result = Lets_play(Memory_agent, random_agent)
        with open("Memory_vs_Random.txt", "a", encoding='utf-8') as f:
            print(result, file=f)
    else:
        print("\n*** Memory Agent vs Random Agent ***")
        result = Lets_play(Memory_agent, random_agent)
        with open("Memory_vs_Random.txt", "x", encoding='utf-8') as f:
            print(result, file=f)

    #Memory vs Fixed
    if os.path.lexists(r"/A_I_course\lab1_code\Memory_vs_Fixed.txt"):
        print("\n*** Memory Agent vs Fixed Agent ***")
        result=Lets_play(Memory_agent,fixed_agent)
        with open("Memory_vs_Fixed.txt","a",encoding='utf-8') as f:
            print(result,file=f)
    else:
        print("\n*** Memory Agent vs Fixed Agent ***")
        result = Lets_play(Memory_agent, fixed_agent)
        with open("Memory_vs_Fixed.txt", "x", encoding='utf-8') as f:
            print(result, file=f)

    #Memory_vs_reflex
    if os.path.lexists(r"/A_I_course\lab1_code\Memory_vs_Reflex.txt"):
        print("\n*** Memory Agent vs reflex Agent ***")
        result = Lets_play(Memory_agent, reflex_agent)
        with open("Memory_vs_Reflex.txt", "a", encoding='utf-8') as f:
            print(result, file=f)
    else:
        print("\n*** Memory Agent vs reflex Agent ***")
        result = Lets_play(Memory_agent, reflex_agent)
        with open("Memory_vs_Reflex.txt", "x", encoding='utf-8') as f:
            print(result, file=f)



if __name__=="__main__":
    main()





