import random 
import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image


# class cards(Image):
#     pass

class Player():
    def __init__(self):
        self.player_cards = []

    def add_card(self, card):
        self.player_cards.append(card)

    def remove_card(self, card):
        self.player_cards.remove(card)

class InGame(FloatLayout):

    def __init__(self, **kwargs):
        super(InGame, self).__init__(**kwargs)
        self.card_deck = [i+1 for i in range(52)]
        self.players = [Player() for i in range(4)]

        for player in self.players:
            for i in range(7):
                card = random.choice(self.card_deck)
                self.card_deck.remove(card)
                player.add_card(card)

        self.display_cards()

    def display_cards(self):

        increment = 1

        for card in self.players[0].player_cards:

            number = str(card % 13)
            if (number == '0'): number = '13'

            suit = card // 13
            if (suit == 0): suit = 'c'
            elif (suit == 1): suit = 'd'
            elif (suit == 2): suit = 'h'
            else: suit = 's'

            img_src = './cards/' + suit + number + '.png'
            self.add_widget(Image(source=img_src, size_hint_y=0.2, pos_hint={'x':increment*0.05}))
            increment += 1

        # self.ids.image.source = 'c1.png'
    
class HoolaApp(App):
    def build(self):
        game = InGame()
        # InGame.photo(game)
        return game

if __name__ == '__main__':
    HoolaApp().run()