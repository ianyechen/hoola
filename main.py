import random 
import kivy

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty

from rotated_cards import RotatedCards
from touch import Touch
from player import Player
from funcs import cardnum_to_cardstr, is_meld_valid, player_turn

# class cards(Image):
#     pass

class InGame(FloatLayout):

    def __init__(self, **kwargs):
        super(InGame, self).__init__(**kwargs)
        self.card_deck = [i+1 for i in range(52)]
        self.players = [Player() for i in range(4)]
        self.widgets = []

        for player in self.players:
            for i in range(7):
                card = random.choice(self.card_deck)
                self.card_deck.remove(card)
                player.add_card(card)

        # for player in self.players:
            # print(player.player_cards)

        self.add_widget(Touch())
        self.display_cards()
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

        self.add_widget(Image(source='./cards/back.png', size_hint_y=0.2, pos_hint={'x': -0.1, 'y':0.5}))
        self.trash_pile_card = Image(source='./cards/back.png', size_hint_y=0.2, pos_hint={'x': 0.1, 'y':0.5})
        self.add_widget(self.trash_pile_card)

        increment = -(len(self.players[0].player_cards)//2) 

        for card in self.players[0].player_cards:

            img_src = cardnum_to_cardstr(card)
            wid = Image(source=img_src, size_hint_y=0.2, pos_hint={'x':increment*0.05, 'y': 0.0})
            self.widgets.append(wid)
            self.add_widget(wid)
            increment += 1

        # self.ids.image.source = 'c1.png'

    def start_game(self):
        card = random.choice(self.card_deck)
        self.trash_pile_card.source = cardnum_to_cardstr(card)
        self.turn = 0
        self.game_over = False
        # while not self.game_over:
        #     print('Currently turn number', self.turn)
        #     player_turn(self.turn)
        #     self.turn += 1
        #     if self.turn == 4: self.turn = 0



    def verify_meld(self):
        cards_currently_selected = []
        for i in range(len(self.players[0].player_cards)):
            if self.children[i].pos_hint['y'] == 0.05: 
                card_str = self.children[i].source[8:]
                card_str = card_str.split('.')[0]
                cards_currently_selected.append(card_str)

        # print(is_meld_valid(cards_currently_selected))


    
class HoolaApp(App):
    def build(self):
        game = InGame()
        # InGame.photo(game)
        return game

if __name__ == '__main__':
    HoolaApp().run()