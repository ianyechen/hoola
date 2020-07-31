from kivy.uix.widget import Widget
from kivy.uix.image import Image

from funcs import cardnum_to_cardstr

class Player(Widget):
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