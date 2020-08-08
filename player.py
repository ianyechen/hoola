from kivy.uix.widget import Widget
from kivy.uix.image import Image

from funcs import cardnum_to_cardstr
from rotated_cards import RotatedCards

class Player(Widget):

    # list of cards that player currently has on hand
    player_cards = []
    # list of combinations of cards that player has melded
    player_melded_cards = []

    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.player_cards = []
        self.player_melded_cards = []

    def add_card(self, card):
        self.player_cards.append(card)

    def remove_card(self, card):
        self.player_cards.remove(card)

    def display_card(self, player_number):
        
        increment = -(len(self.player_cards)//2) 
        if player_number == 2 or player_number == 3: increment += 10

        if player_number == 0:
            for card in self.player_cards:
                img_src = cardnum_to_cardstr(card)
                wid = Image(source=img_src, size_hint_y=0.2, pos_hint={'x':increment*0.05, 'y': 0})
                self.parent.add_widget(wid)
                self.parent.widgets[0].append(wid)
                increment += 1     

        elif player_number == 1:
            for card in self.player_cards:
                wid = Image(source='./cards/back.png', size_hint_y=0.1, pos_hint={'x':increment*0.05, 'y': 0.95})
                self.parent.add_widget(wid)
                self.parent.widgets[1].append(wid)
                increment += 1

        elif player_number == 2:
            for card in self.player_cards:
                wid = RotatedCards(source='./cards/back.png', size_hint_y=0.1, pos_hint={'x':-0.5, 'y': increment*0.05})
                self.parent.add_widget(wid)
                self.parent.widgets[2].append(wid)
                increment += 1

        else:
            for card in self.player_cards:
                wid = RotatedCards(source='./cards/back.png', size_hint_y=0.1, pos_hint={'x':0.5, 'y': increment*0.05})
                self.parent.add_widget(wid)
                self.parent.widgets[3].append(wid)
                increment += 1

    def player_turn(self, player_number):
        
        print('Turn number ', player_number)
        # print(self.player_cards)
        self.parent.draw_card(self)
        if (player_number != 0):
            self.decide_can_meld(player_number)
        # print(self.player_cards)
        self.parent.end_turn(player_number)
        self.parent.refresh_cards(player_number)
        # print(self.player_cards)
        # return player_number + 1 if (player_number + 1 != 4) else 0 

    def decide_can_meld(self, player_number):

        print('Melding for player, ', player_number)
        self.player_cards.sort()

        # key is the number of card (1-13), value is the index where the number is at
        num_to_index = {}
        combinations_that_can_be_melded = []
        copy_of_player_cards = list(self.player_cards)

        # converting the entire list of player cards into the numbers by % 13 (27 -> 1)
        for i in range(len(copy_of_player_cards)):
            copy_of_player_cards[i] %= 13
            if copy_of_player_cards[i] == 0: copy_of_player_cards[i] = 13
            if num_to_index.get(copy_of_player_cards[i]) == None:
                num_to_index[copy_of_player_cards[i]] = []
            num_to_index[copy_of_player_cards[i]].append(i)

        print('Player cards ->', copy_of_player_cards)

        same_suit_cards = []

        for i in range(len(copy_of_player_cards)):

            same_suit_cards.append(copy_of_player_cards[i])

            if i + 1 < len(copy_of_player_cards) and copy_of_player_cards[i+1] < copy_of_player_cards[i]:
                
                print('same suit cards -> ', same_suit_cards)
                if len(same_suit_cards) == 3:

                    # for j in range(len(same_suit_cards)):

                    if ((same_suit_cards[2] == same_suit_cards[1] + 1 == same_suit_cards[0] + 2) 
                    or (12 in same_suit_cards and 13 in same_suit_cards and 1 in same_suit_cards)
                    or (13 in same_suit_cards and 1 in same_suit_cards and 2 in same_suit_cards)):
                        self.player_melded_cards.append(same_suit_cards)

                same_suit_cards = []

        # getting all the 7's 
        if num_to_index.get(7) != None:
            for i in range(len(num_to_index[7])):
                num_to_index[7][i] = self.player_cards[num_to_index[7][i]]

            self.player_melded_cards.append(num_to_index[7])

        # getting the combinations of 3 of the same card 
        for key, value in num_to_index.items():
            if len(value) >= 3:
                for i in range(len(value)):
                    value[i] = self.player_cards[value[i]]

                self.player_melded_cards.append(value)

        if self.player_melded_cards: self.display_melded_cards(player_number)
        print('Melded cards -> ', self.player_melded_cards)
        print('Player cards -> ', self.player_cards)

    def display_melded_cards(self, player_number):

        increment_x = 0
        increment_y = 0
        pos_hint = {}

        for combination in self.player_melded_cards:        

            for card in combination:

                img_src = cardnum_to_cardstr(card)     

                if player_number == 1:
                    pos_hint = {'x':-0.2 + increment_x*0.05, 'y': 0.75}

                elif player_number == 2: 
                    pos_hint = {'x':-0.4 + increment_x*0.05, 'y': 0.5 - increment_y*0.15}
        
                elif player_number == 3:
                    pos_hint = {'x':0.3 + increment_x*0.05, 'y': 0.5 - increment_y*0.15}

                self.parent.add_widget(Image(source=img_src, size_hint_y=0.15, pos_hint=pos_hint))
                increment_x += 1
                if card in self.player_cards: self.player_cards.remove(card)

            if player_number > 1: increment_x = 0
            increment_y += 1