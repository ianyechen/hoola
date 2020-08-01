import random 
import kivy

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty

from rotated_cards import RotatedCards
from touch import Touch
from player import Player
from funcs import cardnum_to_cardstr, cardstr_to_cardnum, is_meld_valid, is_end_turn_valid

class InGame(FloatLayout):

    # indicates whether or not the first card has been taken for a turn (0 for no, 1 for yes)
    taking_first_card = NumericProperty(0)
    number_of_cards_left = NumericProperty(0)
    # the entire card deck left for players to draw from 
    card_deck = []
    # holds the 4 Player classes 
    players = []
    # holds the current player's widgets for displaying the cards
    widgets = []
    # holds the cards currently selected by the player in string ('h13')
    cards_currently_selected = []

    def __init__(self, **kwargs):
        super(InGame, self).__init__(**kwargs)
        self.card_deck = [i+1 for i in range(52)]
        self.players = [Player() for i in range(4)]
      
        # initial distribution of cards at the beginning of game 
        for player in self.players:
            self.add_widget(player)
            for i in range(7):
                card = random.choice(self.card_deck)
                self.card_deck.remove(card)
                player.add_card(card)

        self.add_widget(Touch())
        self.display_cards()
        self.number_of_cards_left = len(self.card_deck)
        self.start_game()

    def display_cards(self):

        increment = -(len(self.players[1].player_cards)//2) 

        for card in self.players[1].player_cards:
            self.add_widget(Image(source='./cards/back.png', size_hint_y=0.1, pos_hint={'x':increment*0.05, 'y': 0.9}))
            increment += 1

        increment = -(len(self.players[2].player_cards)//2) + 10

        for card in self.players[2].player_cards:
            self.add_widget(RotatedCards(source='./cards/back.png', size_hint_y=0.1, pos_hint={'x':-0.5, 'y': increment*0.05}))
            increment += 1

        increment = -(len(self.players[3].player_cards)//2) + 10

        for card in self.players[3].player_cards:
            self.add_widget(RotatedCards(source='./cards/back.png', size_hint_y=0.1, pos_hint={'x':0.5, 'y': increment*0.05}))
            increment += 1

        self.trash_pile_card = Image(source='./cards/back.png', size_hint_y=0.2, pos_hint={'x': 0.1, 'y':0.5})
        self.add_widget(self.trash_pile_card)

        self.players[0].display_card()

    def start_game(self):
        card = random.choice(self.card_deck)
        self.trash_pile_card.source = cardnum_to_cardstr(card)
        self.trash_pile_card_num = card
        self.turn = 0
        self.game_over = False
    
    def verify_meld(self):
        if is_meld_valid(self.cards_currently_selected):
            print('Meld is succesful')

            increment = len(self.players[0].player_melded_cards)
            print(self.players[0].player_melded_cards)

            for card in self.cards_currently_selected:             
                if card == '': continue
                img_src = './cards/' + card + '.png'
                self.add_widget(Image(source=img_src, size_hint_y=0.15, pos_hint={'x':-0.3 + increment*0.05, 'y': 0.25}))

                card_num = cardstr_to_cardnum(card)
                self.players[0].remove_card(card_num)
                self.players[0].player_melded_cards.append(card)
                self.refresh_cards()
                increment += 1

            self.cards_currently_selected.clear()
            self.players[0].player_melded_cards.append('')

    def end_turn(self, turn_num):
        if turn_num != 0:
            card = self.players[turn_num].player_cards[0]
            self.players[turn_num].remove_card(card)
            self.trash_pile_card.source = cardnum_to_cardstr(card)
            self.trash_pile_card_num = card
            return 

        if not is_end_turn_valid(self.cards_currently_selected): return 
        card_num = cardstr_to_cardnum(self.cards_currently_selected[0])
        print(cardstr_to_cardnum(self.cards_currently_selected[0]))
        self.players[0].remove_card(card_num)
        self.trash_pile_card.source = cardnum_to_cardstr(card_num)
        self.trash_pile_card_num = card_num
        self.refresh_cards()
        self.turn += 1

        while self.turn != 0:
            print(self.turn)
            self.turn = self.players[self.turn].player_turn(self.turn)
            self.check_for_thank_yous()


        self.taking_first_card = 0

    def draw_card(self, player):
        self.taking_first_card = 1
        self.cards_currently_selected.clear()
        random_card = random.choice(self.card_deck)
        player.add_card(random_card)
        self.card_deck.remove(random_card)
        self.number_of_cards_left = len(self.card_deck)
        self.refresh_cards()
        
    def thank_you(self):
        self.taking_first_card = 1
        self.cards_currently_selected.clear()
        self.players[0].add_card(self.trash_pile_card_num)
        self.refresh_cards()

    def refresh_cards(self):
        for widget in self.widgets:
            self.remove_widget(widget)
        
        self.players[0].display_card()

    def check_for_thank_yous(self):
        print('checking for thank yous')
    
class HoolaApp(App):
    def build(self):
        return InGame()

if __name__ == '__main__':
    HoolaApp().run()