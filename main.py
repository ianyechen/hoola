import kivy
import random 

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty, BooleanProperty
from kivy.clock import Clock 

from rotated_cards import RotatedCards
from touch import Touch
from player import Player
from funcs import cardnum_to_card_image_path, cardstr_to_cardnum, is_meld_valid, is_add_valid, is_end_turn_valid

class InGame(FloatLayout):

    # indicates whether or not the first card has been taken for a turn 
    took_first_card = BooleanProperty(False)
    # number of cards left in the entire deck 
    number_of_cards_left = NumericProperty(0)
    # whether to hide the buttons or display
    buttons_visible = BooleanProperty(True)
    # whether player is deciding a thank you or not (shows the pass or thank you button)
    deciding_thank_you = BooleanProperty(False)
    # the entire card deck left for players to draw from 
    card_deck = []
    # holds the 4 Player classes 
    players = []
    # holds the current player's widgets for displaying the cards in hand
    widgets_for_player_cards = [[],[],[],[]]
    # holds the current player's widgets for displaying the cards that were melded
    widgets_for_player_melds = [[],[],[],[]]
    # holds the cards currently selected by the player in string ('h13')
    cards_currently_selected = []
    # holds which turn it is (0-3)
    turn = NumericProperty(0)

    def __init__(self, **kwargs):
        super(InGame, self).__init__(**kwargs)
        self.card_deck = [i+1 for i in range(52)]
        self.players = [Player() for i in range(4)]
      
        # initial distribution of cards at the beginning of game 
        count = 0
        for player in self.players:
            self.add_widget(player)

            # if count == 0:
            #     player.player_cards = [1,2,3,4,11,12,13]
            #     for card in player.player_cards:
            #         self.card_deck.remove(card)
            #     count+=1
            #     continue
            # if count == 1:
            #     player.player_cards = [1,14,27, 3,4,5,7]
            #     for card in player.player_cards:
            #         self.card_deck.remove(card)
            #     count+=1
            #     continue

            for i in range(7):
                card = random.choice(self.card_deck)
                self.card_deck.remove(card)
                player.add_card(card)
            
            count+=1

        self.add_widget(Touch())
        self.display_cards()
        self.number_of_cards_left = len(self.card_deck)
        self.start_game()

    def display_cards(self):
        for i in range(4):
            self.players[i].display_card(i)

        self.trash_pile_card = Image(source='./cards/back.png', size_hint_y=0.2, pos_hint={'x': 0.1, 'y':0.5})
        self.add_widget(self.trash_pile_card)

    def start_game(self):
        card = random.choice(self.card_deck)
        self.trash_pile_card.source = cardnum_to_card_image_path(card)
        self.trash_pile_card_num = card
        self.card_deck.remove(card)
        self.turn = 0
        self.game_over = False
    
    def verify_meld(self):
        if is_meld_valid(self.cards_currently_selected):
            print('Meld is succesful')
            increment = len(self.players[0].player_melded_cards)
         
            # displaying melded cards for player 0
            for card in self.cards_currently_selected:             
                if card == '': continue
                img_src = './cards/' + card + '.png'
                self.add_widget(Image(source=img_src, size_hint_y=0.15, pos_hint={'x':-0.3 + increment*0.05, 'y': 0.25}))

                card_num = cardstr_to_cardnum(card)
                self.players[0].remove_card(card_num)
                self.players[0].player_melded_cards.append(card)
                self.refresh_cards(0)
                increment += 1

            self.cards_currently_selected.clear()
            self.players[0].player_melded_cards.append('')

        else:
            # needs to have melded before adding to other combinations 
            if len(self.players[0].player_melded_cards) == 0: 
                print('Add failed. Has to meld own cards first before adding')
                return

            check_meld_turn = 1
            while check_meld_turn < 4:
                valid, melded_cards_index = is_add_valid(self.cards_currently_selected, self.players[check_meld_turn].player_melded_cards) 
                
                if (valid): 
                    print('Add successful!', check_meld_turn, melded_cards_index)
                    for card in self.cards_currently_selected:             
                        card_num = cardstr_to_cardnum(card)
                        self.players[0].remove_card(card_num)
                        self.players[check_meld_turn].player_melded_cards[melded_cards_index].append(card_num)
                        self.refresh_cards(0)

                    self.cards_currently_selected.clear()
                    self.players[check_meld_turn].display_melded_cards(check_meld_turn)
                    self.update_melds(check_meld_turn)
                    break

                check_meld_turn += 1
            
    def end_turn(self, turn_num):

        if turn_num != 0:
            card = self.players[turn_num].player_cards[0]
            self.players[turn_num].remove_card(card)
            self.trash_pile_card.source = cardnum_to_card_image_path(card)
            self.trash_pile_card_num = card
            self.check_for_game_over(turn_num)
            self.deciding_thank_you = True
            self.buttons_visible = True
            self.check_for_thank_yous()
            return 

        if not is_end_turn_valid(self.cards_currently_selected): return 

        card_num = cardstr_to_cardnum(self.cards_currently_selected[0])
        self.players[0].remove_card(card_num)
        self.trash_pile_card.source = cardnum_to_card_image_path(card_num)
        self.trash_pile_card_num = card_num
        self.check_for_game_over(turn_num)
        self.refresh_cards(0)
        self.buttons_visible = False
        self.took_first_card = False
        self.turn += 1
        self.players[self.turn].player_turn(self.turn)

    def draw_card(self, player):
        self.took_first_card = True
        self.cards_currently_selected.clear()
        random_card = random.choice(self.card_deck)
        player.add_card(random_card)
        self.card_deck.remove(random_card)
        self.number_of_cards_left = len(self.card_deck)
        self.refresh_cards(0)

    def refresh_cards(self, player_number):
        for widget in self.widgets_for_player_cards[player_number]:
            self.remove_widget(widget)

        self.widgets_for_player_cards[player_number].clear()        
        self.players[player_number].display_card(player_number)

    def update_melds(self, player_number):
        for widget in self.widgets_for_player_melds[player_number]:
            self.remove_widget(widget)

        self.widgets_for_player_melds[player_number].clear()        
        self.players[player_number].display_melded_cards(player_number)

    def check_for_thank_yous(self):
        Clock.schedule_interval(self.set_deciding_thank_you, 0.1)

    def set_deciding_thank_you(self, dt):
        if not self.deciding_thank_you:
            Clock.unschedule(self.set_deciding_thank_you)  

    def thank_you(self):
        self.took_first_card = True
        self.turn = 0
        self.cards_currently_selected.clear()
        self.players[0].add_card(self.trash_pile_card_num)
        self.refresh_cards(0)
        self.trash_pile_card.source = './cards/back.png'
        self.trash_pile_card_num = None
        self.deciding_thank_you = False

    def pass_for_thank_you(self):
        self.deciding_thank_you = False
        self.buttons_visible = False 
        self.turn += 1

        if self.turn == 4:
            self.turn = 0
            self.buttons_visible = True
            self.took_first_card = False
            return

        self.players[self.turn].player_turn(self.turn)

    def check_for_game_over(self, turn_num):
        if len(self.players[turn_num].player_cards) == 0:
            print('Game over. Player', turn_num, 'won!')
            return True
        else: return False

class HoolaApp(App):
    def build(self):
        return InGame()

if __name__ == '__main__':
    HoolaApp().run()