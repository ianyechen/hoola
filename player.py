from kivy.uix.widget import Widget
from kivy.uix.image import Image

from funcs import cardnum_to_card_image_path, cardnum_to_cardstr, cardstr_to_cardnum, is_add_valid, cardnum_dict_to_cardstr_dict
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
        
        game_log_string = "Player " + str(player_number) + "'s turn\n"
        self.parent.game_log.game_log += game_log_string
        print('-------------------------------------------', 'Starting Turn number', player_number, '-------------------------------------------')
        self.parent.draw_card(self)

        if (player_number != 0):

            self.decide_can_meld(player_number, False)

            if len(self.player_melded_cards) != 0:

                check_meld_turn = 0
                check_same_player_again = False

                while check_meld_turn < 4:

                    for card in self.player_cards:

                        cards_currently_selected = [cardnum_to_cardstr(card)]
                        valid, melded_cards_index = is_add_valid(cards_currently_selected, self.parent.players[check_meld_turn].player_melded_cards) 

                        if (valid): 
                            game_log_string = "Player " + str(player_number) + " added " + str(cardnum_to_cardstr(card)) + " to Player " + str(check_meld_turn) + "\n"
                            self.parent.game_log.game_log += game_log_string
                            print('Player' , player_number, 'added', card, 'to Player', check_meld_turn)
                            for card in cards_currently_selected:             
                                card_num = cardstr_to_cardnum(card)
                                self.parent.players[player_number].remove_card(card_num)
                                self.parent.players[check_meld_turn].player_melded_cards[melded_cards_index].append(card_num)
                                self.parent.players[check_meld_turn].player_melded_cards[melded_cards_index].sort()
                                self.parent.refresh_cards(player_number)

                            self.parent.players[check_meld_turn].display_melded_cards(check_meld_turn)
                            self.parent.update_melds(check_meld_turn)
                            check_same_player_again = True

                    if not check_same_player_again: check_meld_turn += 1
                    check_same_player_again = False
                
        if self.parent.check_for_game_over(player_number, False): return
        self.parent.end_turn(player_number)
        self.parent.refresh_cards(player_number)

    def decide_can_meld(self, player_number, saying_thank_you):

        # if not saying_thank_you: print('Melding for player, ', player_number)
        player_cards_before_sort = list(self.player_cards)
        self.player_cards.sort()
        can_say_thank_you = False

        # key is the number of card (1-13), value is the index where the number is at
        num_to_index = {}
        copy_of_player_cards = list(self.player_cards)
        # print('Player Cards -> ', copy_of_player_cards)

        # converting the entire list of player cards into the numbers by % 13 (27 -> 1)
        for i in range(len(copy_of_player_cards)):
            copy_of_player_cards[i] = cardnum_to_cardstr(copy_of_player_cards[i])
            if num_to_index.get(copy_of_player_cards[i][1:]) == None:
                num_to_index[copy_of_player_cards[i][1:]] = []
            num_to_index[copy_of_player_cards[i][1:]].append(i)

        same_suit_cards = []
        melded_consecutive_cards = False

        for i in range(len(copy_of_player_cards)):

            same_suit_cards.append(copy_of_player_cards[i])

            # if next card is of different suit or this is the last iteration of the loop (checking last card)
            if (i + 1 < len(copy_of_player_cards) and copy_of_player_cards[i+1][0] != copy_of_player_cards[i][0]) or (i == len(copy_of_player_cards) - 1):
                
                if len(same_suit_cards) >= 3:
                    
                    suit_str = same_suit_cards[0][0]

                    for i in range(len(same_suit_cards)):
                        same_suit_cards[i] = int(same_suit_cards[i][1:])
                    
                    # using a left and right system to check every single index 
                    consecutive_cards = set()
                    loop = False
                    left = 0 
                    right = len(same_suit_cards) - 1

                    # if 1, 2, 13 in list
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
                        
                    # if 1, 12, 13 in list
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
                        if saying_thank_you:
                            for count, card in enumerate(list_to_add):
                                num = cardstr_to_cardnum(suit_str+str(card))
                                if num == self.parent.trash_pile_card_num: can_say_thank_you = True
                            
                        else:
                            copy_of_list_to_add = list(list_to_add)
                            game_log_string = "Player " + str(player_number) + " melded " + str(cardnum_dict_to_cardstr_dict(copy_of_list_to_add)) + "\n"
                            self.parent.game_log.game_log += game_log_string
                            for count, card in enumerate(list_to_add):
                                num = cardstr_to_cardnum(suit_str+str(card))
                                list_to_add[count] = num
                                self.player_cards.remove(num)        
                            list_to_add.sort()
                            self.player_melded_cards.append(list_to_add)
                            
                            print('Player', player_number, 'melded', list_to_add)

                            consecutive_cards.clear()
                            melded_consecutive_cards = True
                        
                    # checking to see if there are any other combinations, or if there wasn't a loop
                    while (left <= right):
                        if left != right and (same_suit_cards[left+1] == same_suit_cards[left] + 1): 
                            consecutive_cards.add(same_suit_cards[left])
                            consecutive_cards.add(same_suit_cards[left+1])
                        else:
                            if len(consecutive_cards) >= 3: 
                                list_to_add = list(consecutive_cards)
                                if saying_thank_you:
                                    for count, card in enumerate(list_to_add):
                                        num = cardstr_to_cardnum(suit_str+str(card))
                                        if num == self.parent.trash_pile_card_num: can_say_thank_you = True

                                else:
                                    game_log_string = "Player " + str(player_number) + " melded " + str(list_to_add) + "\n"
                                    self.parent.game_log.game_log += game_log_string
                                    for count, card in enumerate(list_to_add):
                                        num = cardstr_to_cardnum(suit_str+str(card))
                                        list_to_add[count] = num
                                        self.player_cards.remove(num)         
                                    list_to_add.sort()
                                    self.player_melded_cards.append(list_to_add)
                                    
                                    print('Player', player_number, 'melded', list_to_add)

                                    melded_consecutive_cards = True
                            consecutive_cards.clear()

                        left += 1
    
                same_suit_cards = []

        # needs to refresh num_to_index if some cards have been melded already 
        if melded_consecutive_cards:
            copy_of_player_cards = list(self.player_cards)
            num_to_index.clear()
            for i in range(len(copy_of_player_cards)):
                copy_of_player_cards[i] = cardnum_to_cardstr(copy_of_player_cards[i])
                if num_to_index.get(copy_of_player_cards[i][1:]) == None:
                    num_to_index[copy_of_player_cards[i][1:]] = []
                num_to_index[copy_of_player_cards[i][1:]].append(i)

        melded_sevens_alone = False

        # print('num_to_index -> ', num_to_index)

        # getting all the 7's 
        if num_to_index.get('7') != None and not saying_thank_you:
            melded_sevens_alone = True
            for i in range(len(num_to_index['7'])):
                num_to_index['7'][i] = self.player_cards[num_to_index['7'][i]]
                meld_combo_with_single_seven = [num_to_index['7'][i]]
                self.player_melded_cards.append(meld_combo_with_single_seven)
                copy_of_meld_combo_with_single_seven = list(meld_combo_with_single_seven)
                game_log_string = "Player " + str(player_number) + " melded " + str(cardnum_dict_to_cardstr_dict(copy_of_meld_combo_with_single_seven)) + "\n"
                self.parent.game_log.game_log += game_log_string
                print('Player', player_number, 'melded', meld_combo_with_single_seven)

            for i in range(len(num_to_index['7'])):
                self.player_cards.remove(num_to_index['7'][i])

        if melded_sevens_alone:
            copy_of_player_cards = list(self.player_cards)
            num_to_index.clear()
            for i in range(len(copy_of_player_cards)):
                copy_of_player_cards[i] = cardnum_to_cardstr(copy_of_player_cards[i])
                if num_to_index.get(copy_of_player_cards[i][1:]) == None:
                    num_to_index[copy_of_player_cards[i][1:]] = []
                num_to_index[copy_of_player_cards[i][1:]].append(i)

        # getting the combinations of 3 of the same card 
        for key, value in num_to_index.items():
            if key == 7: continue
            if len(value) >= 3:
                if saying_thank_you:
                    for i in range(len(value)):
                        value[i] = self.player_cards[value[i]]
                        if value[i] == self.parent.trash_pile_card_num: can_say_thank_you = True

                else:
                    for i in range(len(value)):
                        value[i] = self.player_cards[value[i]]
                
                    self.player_melded_cards.append(value)
                    copy_of_value = list(value)
                    game_log_string = "Player " + str(player_number) + " melded " + str(cardnum_dict_to_cardstr_dict(copy_of_value)) + "\n"
                    self.parent.game_log.game_log += game_log_string
                    print('Player', player_number, 'melded', value)

                    for i in range(len(value)):
                        self.player_cards.remove(value[i])

        if saying_thank_you: 
            self.player_cards = player_cards_before_sort 
            return can_say_thank_you
        if self.player_melded_cards: self.display_melded_cards(player_number)
      
    def display_melded_cards(self, player_number):

        increment_x = 0
        increment_y = 0
        pos_hint = {}

        for combination in self.player_melded_cards:

            for card in combination:

                img_src = cardnum_to_card_image_path(card)     

                if player_number == 0:
                    pos_hint = {'x':-0.2 + increment_x*0.03, 'y': 0.25}
                
                elif player_number == 1:
                    pos_hint = {'x':-0.2 + increment_x*0.03, 'y': 0.75}

                elif player_number == 2: 
                    pos_hint = {'x':-0.4 + increment_x*0.03, 'y': 0.65 - increment_y*0.15}
        
                elif player_number == 3:
                    pos_hint = {'x':0.3 + increment_x*0.03, 'y': 0.65 - increment_y*0.15}

                wid = Image(source=img_src, size_hint_y=0.15, pos_hint=pos_hint)
                self.parent.add_widget(wid)
                self.parent.widgets_for_player_melds[player_number].append(wid)
                increment_x += 1

            if player_number > 1: increment_x = 0
            else: increment_x += 2 
            increment_y += 1

    def check_for_thank_yous(self, turn_num):

        print('Checking thank you for turn', turn_num)
        self.add_card(self.parent.trash_pile_card_num)

        if self.decide_can_meld(turn_num, True):

            self.parent.turn = turn_num
            game_log_string = "Player " + str(turn_num) + " said thank you to " + str(cardnum_to_cardstr(self.parent.trash_pile_card_num)) + "\n"
            self.parent.game_log.game_log += game_log_string
            print('Player', turn_num , 'can say thank you to', self.parent.trash_pile_card_num)
            self.decide_can_meld(turn_num, False)

            if len(self.player_melded_cards) != 0:
                check_meld_turn = 0
                check_same_player_again = False

                while check_meld_turn < 4:

                    for card in self.player_cards:
                        cards_currently_selected = [cardnum_to_cardstr(card)]
                        valid, melded_cards_index = is_add_valid(cards_currently_selected, self.parent.players[check_meld_turn].player_melded_cards)

                        if (valid): 
                            game_log_string = "Player " + str(turn_num) + " added " + str(cardnum_to_cardstr(card)) + " to Player " + str(check_meld_turn) + "\n"
                            self.parent.game_log.game_log += game_log_string
                            print('Player', turn_num, 'added', card, 'to Player', check_meld_turn)
                            for card in cards_currently_selected:             
                                card_num = cardstr_to_cardnum(card)
                                self.parent.players[turn_num].remove_card(card_num)
                                self.parent.players[check_meld_turn].player_melded_cards[melded_cards_index].append(card_num)
                                self.parent.players[check_meld_turn].player_melded_cards[melded_cards_index].sort()
                                self.parent.refresh_cards(turn_num)

                            self.parent.players[check_meld_turn].display_melded_cards(check_meld_turn)
                            self.parent.update_melds(check_meld_turn)
                            check_same_player_again = True

                    if not check_same_player_again: check_meld_turn += 1
                    check_same_player_again = False

            self.parent.end_turn(turn_num)
            self.parent.refresh_cards(turn_num)
            return True

        else: 
            self.remove_card(self.parent.trash_pile_card_num)
            return False