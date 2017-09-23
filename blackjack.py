import random
from abc import ABCMeta, abstractmethod

card_point_map = {
                    'A': 1,
                    '2': 2,
                    '3': 3,
                    '4': 4,
                    '5': 5,
                    '6': 6,
                    '7': 7,
                    '8': 8,
                    '9': 9,
                    '10': 10,
                    'J': 10,
                    'Q': 10,
                    'K': 10
                }



class decks(object):
   
    single_deck = ([str(i) for i in range(2, 11)] + ['A', 'J', 'Q', 'K']) * 4

    def __init__(self, num_of_decks = 1):       
        self.num_of_decks = num_of_decks
        self.cards = decks.single_deck * num_of_decks
        random.shuffle(self.cards)    
        
    def shuffle(self):
        random.shuffle(self.cards)

    def serve_card(self):
        if not self.cards:
            print("There are no cards left. shuffling new decks")
            self.__init__(self.num_of_decks)
        return self.cards.pop()




class player_abstract(object):

    __metaclass__ = ABCMeta

    def __init__(self, name,  money):
        self.name = name
        self.money = money
        self.hands = []
        self.bet = 0
        self.in_stand = False


    def stand(self):
        self.in_stand = True
        print("%s's points in hand is %s (%s)" % (self.name, self.best_point(), ' '.join(self.hands)))

    def hit(self, card):
        self.hands.append(card) 
        self.show_hands() 

    def best_point(self):
        hands_sum = 0
        for card in self.hands:
            hands_sum += card_point_map[card]
        if 'A' in self.hands and hands_sum <= 11:
            hands_sum += 10
        return hands_sum               

    def win(self, amount = None):
        if amount == None:
            amount = self.bet
        self.money += amount
        # self.__print_transaction__(amount)    DEBUG

    def lose(self, amount = None):
        if amount == None:
            amount = self.bet
        self.money -= amount
        # self.__print_transaction__(amount)    DEBUG

    def new_game(self):
        self.hands = []
        self.bet = 0
        self.in_stand = False

    def display_hands(self):
        print("%s's hands: %s" % (self.name, ' '.join(self.hands)))

    # DEBUG
    def __print_transaction__(self, amount):
        print("%s: transaction amount=%s, current money=%s" % (self.name, amount, self.money))

    @abstractmethod
    def show_hands(self):
        pass




class player(player_abstract):
    def __init__(self, name,  money = 100):
        super(player, self).__init__(name, money)

    def __repr__(self):
        return "Player name=%s, money=%s" % (self.name, self.money)

    def auto_play(self):
        pass

    def show_hands(self):
        print("%s's hands: %s" % (self.name, ', '.join(self.hands)))




class dealer(player_abstract):
    def __init__(self, name = 'Dealer', money = 100000):
        super(dealer, self).__init__(name,  money)

    def auto_play(self, decks):
        while not self.in_stand:
            point_in_hand = self.best_point()
            if point_in_hand <= 16:
                self.hit(decks.serve_card())
            elif point_in_hand <= 21:
                self.stand()
            else:
                print("Dealer has busted!")
                self.peek_dealer_hands()
                break

    def show_hands(self):
        print("Dealer's hands: %s" % ', '.join(self.hands[1:]) + ', X')

    def peek_dealer_hands(self):
        print("Dealer's hands: %s" % ', '.join(self.hands))


def ask_for_bet(player):
    while True:
        try:
            bet = int(raw_input("Please provide the bet for %s: " % player.name))
        except:
            print("Please provide a valid integer as the bet.")
        else:
            if bet > player.money:
                print("The bet needs to be smaller than %s's total money" % player.name)    
            else:
                return bet

def ask_for_action(player):
    while True:
        player_action = raw_input("Action for %s (allowed actions are: stand or hit): " % player.name).strip().lower()
        if player_action in ('hit', 'stand'):
            break
        else:
            print("Please provide an allowed action.")
    return player_action


def initial_server_card(dealer, players, decks):
    for num in range(2):
        for player in players:
            player.hands.append(decks.serve_card())
        dealer.hands.append(decks.serve_card())

    
def check_natural(player):
    ten_card = ['10', 'J', 'Q', 'K']
    return 'A' in player.hands and any(card in player.hands for card in ten_card)


def gaming(dealer, players, decks):

    initial_server_card(dealer, players, decks)

    dealer_natural = check_natural(dealer)
    dealer.show_hands()

    for player in players[:]:        
        player_natural = check_natural(player)
        player.show_hands()

        if dealer_natural and not player_natural:
            player.lose()            
            dealer.win(player.bet)
            players.remove(player)
            print("Dealer has a blackjack, %s lose." % player.name)
        elif player_natural and not dealer_natural:
            player.win(player.bet * 1.5)
            dealer.lose(player.bet)
            players.remove(player)
            print("Dealer does not have a blackjack, %s wins." % player.name)
        elif player_natural and dealer_natural:
            print("Tie: both dealer and %s have a blackjack!" % player.name)
            players.remove(player)
        else:
            continue

    if not players:
        print("Game over")
        return
    
    for player in players[:]:
        if player.best_point() > 21:
            player.lose()            
            dealer.win(player.bet)
            players.remove(player)
            print("Player %s bust, dealer wins." % player.name)
        elif dealer.best_point() > 21:
            player.win()
            dealer.lose(player.bet)
            players.remove(player)
            print("Dealer bust, %s wins." % player.name)
        else:
            while not player.in_stand and player.best_point() < 21:
                player_action = ask_for_action(player)
                if player_action == 'hit':
                    player.hit(decks.serve_card())
                else:
                    player.stand()
            if player.best_point() > 21:
                player.lose()            
                dealer.win(player.bet)
                players.remove(player)
                print("Player %s bust, dealer wins." % player.name)

    if len(players): 
        if not dealer.in_stand:
            dealer.auto_play(decks)
        dealer_points = dealer.best_point()
        for player in players:
            if dealer_points > 21:
                player.win()
                dealer.lose(player.bet)
                print("Dealer bust, %s wins." % player.name)
            elif player.best_point() > dealer_points:
                player.win()
                dealer.lose(player.bet)
                print("%s wins." % player.name)
            elif player.best_point() < dealer_points:
                player.lose()            
                dealer.win(player.bet)
                print("%s lose." % player.name)
            else:
                print("Tie: both Dealer and %s have a %s!" % (player.name, dealer_points)) 

    print("Game over")
    return



if __name__ == '__main__':

    # decks = decks()
    # print(decks.cards)
    # decks.shuffle()
    # print(decks.cards)
    # print(decks.pick_card(), len(decks.cards))
    

    player_num = 2
    all_players = [player('jack', 100), player('mark', 1000)]
    for player in all_players:
        player.bet = 100
    dealer = dealer()
    decks = decks(6)

    # while True:
    #     try:
    #         player_num = int(raw_input("How many players are joining the game(dealer is not included): "))
    #     except:
    #         print("Please input a valid number")
    #         continue
    #     break
    # 
    # all_players = []
    # print("Please input name and initial money for each player, e.g. name money")
    # for num in range(1, player_num+1):
    #     while True:
    #         try:
    #             name, money = raw_input("Player No.%s: " % num).strip().split()
    #         except:
    #             print("Please input valid input for the player.")
    #             continue
    #         else:
    #             all_players.append(player(name = name, money = int(money)))
    #             break
    # 
    # dealer = dealer()
    # decks = decks()
    # 
    existing_players = all_players[:]
    while True:        
        print("List of current players:")
        for player in existing_players[:]:
            if player.money < player.bet:
                print("DEBUG: player %s money = %s, bet = %s" % (player.name, player.money, player.bet))
                existing_players.remove(player)
                continue
            print("%s's current money: %s" % (player.name, player.money))                
            player.new_game()
            #player.bet = ask_for_bet(player)
            player.bet = 100  #TODO: debug code 
        dealer.new_game()
        gaming(dealer, existing_players[:], decks)

        continue_play = raw_input("Do you want to play blackjack? (Y or N)")
        if continue_play.strip().upper() == 'N':
            break