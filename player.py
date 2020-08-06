from kivy.uix.widget import Widget
from kivy.uix.image import Image

from funcs import cardnum_to_cardstr

class Player(Widget):

    # list of cards that player currently has on hand
    player_cards = []
    # list of combinations of cards that player has melded
    player_melded_cards = []

    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.player_cards = []

    def add_card(self, card):
        self.player_cards.append(card)

    def remove_card(self, card):
        self.player_cards.remove(card)

    def display_card(self):

        increment = -(len(self.player_cards)//2) 

        for card in self.player_cards:
            img_src = cardnum_to_cardstr(card)
            wid = Image(source=img_src, size_hint_y=0.2, pos_hint={'x':increment*0.05, 'y': 0})
            self.parent.add_widget(wid)
            self.parent.widgets.append(wid)
            increment += 1        

    def player_turn(self, player_number):
        
        print('Turn number ', player_number)
        # print(self.player_cards)
        self.parent.draw_card(self)
        if (player_number != 0):
            self.decide_can_meld(player_number)
        # print(self.player_cards)
        self.parent.end_turn(player_number)
        # print(self.player_cards)
        # return player_number + 1 if (player_number + 1 != 4) else 0 

    def decide_can_meld(self, player_number):

        print('Melding for player, ', player_number)
        self.player_cards.sort()
        num_to_index = {}
        combinations_that_can_be_melded = []
        copy_of_player_cards = list(self.player_cards)

        print('Player cards ->', self.player_cards)
        for i in range(len(copy_of_player_cards)):
            copy_of_player_cards[i] %= 13
            if copy_of_player_cards[i] == 0: copy_of_player_cards[i] = 13
            if num_to_index.get(copy_of_player_cards[i]) == None:
                num_to_index[copy_of_player_cards[i]] = []
            num_to_index[copy_of_player_cards[i]].append(i)

        print('Player cards ->', self.player_cards)
        print('Player cards copy ->', copy_of_player_cards)
        print(num_to_index)

        if num_to_index.get(7) != None:
            combinations_that_can_be_melded.append(num_to_index[7])

        for key, value in num_to_index.items():
            if len(value) >= 3:
                combinations_that_can_be_melded.append(value)


        print(combinations_that_can_be_melded)


