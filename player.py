from kivy.uix.widget import Widget
from kivy.uix.image import Image

from funcs import cardnum_to_card_image_path, cardnum_to_cardstr, cardstr_to_cardnum
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
                img_src = cardnum_to_card_image_path(card)
                wid = Image(source=img_src, size_hint_y=0.2, pos_hint={'x':increment*0.05, 'y': 0})
                self.parent.add_widget(wid)
                self.parent.widgets_for_player_cards[0].append(wid)

                increment += 1     

        elif player_number == 1:
            for card in self.player_cards:
                wid = Image(source='./cards/back.png', size_hint_y=0.1, pos_hint={'x':increment*0.05, 'y': 0.95})
                self.parent.add_widget(wid)
                self.parent.widgets_for_player_cards[1].append(wid)
                increment += 1

        elif player_number == 2:
            for card in self.player_cards:
                wid = RotatedCards(source='./cards/back.png', size_hint_y=0.1, pos_hint={'x':-0.5, 'y': increment*0.05})
                self.parent.add_widget(wid)
                self.parent.widgets_for_player_cards[2].append(wid)
                increment += 1

        else:
            for card in self.player_cards:
                wid = RotatedCards(source='./cards/back.png', size_hint_y=0.1, pos_hint={'x':0.5, 'y': increment*0.05})
                self.parent.add_widget(wid)
                self.parent.widgets_for_player_cards[3].append(wid)
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
        # combinations_that_can_be_melded = []
        copy_of_player_cards = list(self.player_cards)

        # converting the entire list of player cards into the numbers by % 13 (27 -> 1)
        for i in range(len(copy_of_player_cards)):
            copy_of_player_cards[i] = cardnum_to_cardstr(copy_of_player_cards[i])
            # if copy_of_player_cards[i] == 0: copy_of_player_cards[i] = 13
            if num_to_index.get(copy_of_player_cards[i][1:]) == None:
                num_to_index[copy_of_player_cards[i][1:]] = []
            num_to_index[copy_of_player_cards[i][1:]].append(i)

        print('Player cards ->', copy_of_player_cards)
        print('num_to_index ->', num_to_index)

        same_suit_cards = []
        
        melded_consecutive_cards = False

        for i in range(len(copy_of_player_cards)):

            same_suit_cards.append(copy_of_player_cards[i])
            print(same_suit_cards)
            # if next card is of different suit or this is the last iteration of the loop (checking last card)
            if (i + 1 < len(copy_of_player_cards) and copy_of_player_cards[i+1][0] != copy_of_player_cards[i][0]) or (i == len(copy_of_player_cards) - 1):
                
                print('same suit cards -> ', same_suit_cards)
                if len(same_suit_cards) >= 3:
                    
                    suit_str = same_suit_cards[0][0]

                    for i in range(len(same_suit_cards)):
                        same_suit_cards[i] = int(same_suit_cards[i][1:])

                    
                    consecutive_cards = set()
                    loop = False
                    left = 0 
                    right = len(same_suit_cards) - 1

                    if 13 in same_suit_cards and 1 in same_suit_cards and 2 in same_suit_cards:
                        consecutive_cards.update([1, 2, 13])
                        loop = True
                        left += 2
                        right -= 1
                        while (same_suit_cards[left] != 13 and same_suit_cards[left] - 1 == same_suit_cards[left-1]):
                            consecutive_cards.add(same_suit_cards[left])
                            left += 1

                        while (same_suit_cards[right] != 2 and same_suit_cards[right] + 1 == same_suit_cards[right+1]):
                            consecutive_cards.add(same_suit_cards[right])
                            right -= 1 
                        
                    elif 12 in same_suit_cards and 13 in same_suit_cards and 1 in same_suit_cards:
                        consecutive_cards.update([1, 12, 13])
                        loop = True
                        left += 1
                        right -= 2
                        while (same_suit_cards[left] != 12 and same_suit_cards[left] - 1 == same_suit_cards[left-1]):
                            consecutive_cards.add(same_suit_cards[left])
                            left += 1

                        while (same_suit_cards[right] != 1 and same_suit_cards[right] + 1 == same_suit_cards[right+1]):
                            consecutive_cards.add(same_suit_cards[right])
                            right -= 1 

                    if loop:
                        list_to_add = list(consecutive_cards)
                        for card in list_to_add:
                            num = cardstr_to_cardnum(suit_str+str(card))
                            self.player_cards.remove(num)
                        self.player_melded_cards.append(list_to_add)
                        consecutive_cards.clear()
                        melded_consecutive_cards = True
                        
                    while (left <= right):
                        if left != right and (same_suit_cards[left+1] == same_suit_cards[left] + 1): 
                            consecutive_cards.add(same_suit_cards[left])
                            consecutive_cards.add(same_suit_cards[left+1])
                        else:
                            if len(consecutive_cards) >= 3: 
                                list_to_add = list(consecutive_cards)
                                print(list_to_add)
                                print(self.player_cards)
                                for card in list_to_add:
                                    num = cardstr_to_cardnum(suit_str+str(card))
                                    self.player_cards.remove(num)                                
                                self.player_melded_cards.append(list_to_add)
                                melded_consecutive_cards = True
                            consecutive_cards.clear()

                        left += 1
    
                same_suit_cards = []

        if melded_consecutive_cards:
            copy_of_player_cards = list(self.player_cards)
            num_to_index.clear()
            for i in range(len(copy_of_player_cards)):
                copy_of_player_cards[i] = cardnum_to_cardstr(copy_of_player_cards[i])
                if num_to_index.get(copy_of_player_cards[i][1:]) == None:
                    num_to_index[copy_of_player_cards[i][1:]] = []
                num_to_index[copy_of_player_cards[i][1:]].append(i)

        melded_sevens_alone = False
        # getting all the 7's 
        if num_to_index.get('7') != None:
            melded_sevens_alone = True
            print('slkdjskdjf')
            for i in range(len(num_to_index['7'])):
                num_to_index['7'][i] = self.player_cards[num_to_index['7'][i]]
                meld_combo_with_single_seven = [num_to_index['7'][i]]
                self.player_melded_cards.append(meld_combo_with_single_seven)
                self.player_cards.remove(num_to_index['7'][i])
                # print(self.player_melded_cards)

        if melded_sevens_alone:
            copy_of_player_cards = list(self.player_cards)
            num_to_index.clear()
            for i in range(len(copy_of_player_cards)):
                copy_of_player_cards[i] = cardnum_to_cardstr(copy_of_player_cards[i])
                if num_to_index.get(copy_of_player_cards[i][1:]) == None:
                    num_to_index[copy_of_player_cards[i][1:]] = []
                num_to_index[copy_of_player_cards[i][1:]].append(i)

        print('Player cards ->', copy_of_player_cards)
        print('num_to_index ->', num_to_index)
        # getting the combinations of 3 of the same card 
        for key, value in num_to_index.items():
            if key == 7: continue
            if len(value) >= 3:
                for i in range(len(value)):
                    value[i] = self.player_cards[value[i]]
                
                self.player_melded_cards.append(value)
                for i in range(len(value)):
                    self.player_cards.remove(value[i])

        if self.player_melded_cards: self.display_melded_cards(player_number)
        print('Melded cards -> ', self.player_melded_cards)
        print('Player cards -> ', self.player_cards)

    def display_melded_cards(self, player_number):

        increment_x = 0
        increment_y = 0
        pos_hint = {}

        for combination in self.player_melded_cards:        

            for card in combination:

                img_src = cardnum_to_card_image_path(card)     

                if player_number == 1:
                    pos_hint = {'x':-0.2 + increment_x*0.03, 'y': 0.75}

                elif player_number == 2: 
                    pos_hint = {'x':-0.4 + increment_x*0.03, 'y': 0.5 - increment_y*0.15}
        
                elif player_number == 3:
                    pos_hint = {'x':0.3 + increment_x*0.03, 'y': 0.5 - increment_y*0.15}

                wid = Image(source=img_src, size_hint_y=0.15, pos_hint=pos_hint)
                self.parent.add_widget(wid)
                self.parent.widgets_for_player_melds[player_number].append(wid)
                if player_number == 1: increment_x += 2 # spacing between the combinations 
                else: increment_x += 1
                # if card in self.player_cards: self.player_cards.remove(card)

            if player_number > 1: increment_x = 0
            elif player_number == 1: increment_x += 1 
            increment_y += 1